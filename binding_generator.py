#!/usr/bin/python3

import json
import subprocess
import sys


def main(args):
	src = args[1]
	dst = args[2]

	generate_default_functions = "--generate-default-functions" in args
	allow_global_variables = "--allow-global-variables" in args
	infer_enum_name = "--infer-enum-name" in args

	builtin_types = {
		"void": "void",

		"int8_t": "i8",
		"int16_t": "i16",
		"int32_t": "i32",
		"int64_t": "i64",
		"int_least8_t": "i8",
		"int_least16_t": "i16",
		"int_least32_t": "i32",
		"int_least64_t": "i64",
		"int_fast8_t": "i8",
		"int_fast16_t": "i16",
		"int_fast32_t": "i32",
		"int_fast64_t": "i64",

		"uint8_t": "u8",
		"uint16_t": "u16",
		"uint32_t": "u32",
		"uint64_t": "u64",
		"uint_least8_t": "u8",
		"uint_least16_t": "u16",
		"uint_least32_t": "u32",
		"uint_least64_t": "u64",
		"uint_fast8_t": "u8",
		"uint_fast16_t": "u16",
		"uint_fast32_t": "u32",
		"uint_fast64_t": "u64",

		"size_t": "uint",
		"intptr_t": "int",
		"uintptr_t": "uint",
		"ptrdiff_t": "int",
		"intmax_t": "int",
		"uintmax_t": "uint",
		"imaxdiv_t": "int",

		"char": "byte",
		"unsigned char": "u8",
		"short": "i16",
		"unsigned short": "u16",
		"int": "i32",
		"unsigned": "u32",
		"unsigned int": "u32",
		"long": "i32",
		"unsigned long": "u32",
		"long long": "i64",
		"unsigned long long": "u64",

		"float": "f32",
		"double": "f64",
		"long double": "f64",

		"wchar_t": "wchar_t",
		"max_align_t": "max_align_t",

		"uchar": "u8",
		"ushort": "u16",
		"uint": "u32",
		"ulong": "u32",

		"register_t": "register_t",
	}

	def clang(path):
		cmd = ["clang", "-Xclang", "-ast-dump=json", "-c", path]
		return json.loads(subprocess.check_output(cmd))["inner"]

	def parseType(t):
		t = t.strip().replace("struct ", "").replace("enum ", "")

		if t in builtin_types:
			return builtin_types[t]
		elif t[-1] == '*':
			if t.startswith("const "):
				pointee = parseType(t[6:-1])
				if pointee == "void":
					return "ptr!<byte, false>"
				else:
					return "ptr!<" + pointee + ", false>"
			else:
				pointee = parseType(t[:-1])
				if pointee == "void":
					return "ptr!<byte, true>"
				else:
					return "ptr!<" + pointee + ", true>"
		elif t[-1] == ']':
			index_start = t.rfind('[')
			element_type = parseType(t[:index_start])
			size = t[index_start + 1:-1]
			if size == "":
				return "ptr!<" + element_type + ", true>"

			return "Array!<" + element_type + ", " + size + ">"
		elif t.endswith("*const"):
			return "ptr!<" + parseType(t[:-6]) + ", false>"
		elif "(*)" in t:
			sep = t.find("(*)")
			return_type = parseType(t[:sep])
			parameters = [parseType(p) for p in t[sep+4:-1].split(",")]
			return "(" + ", ".join(parameters) + ")" + " -> " + return_type
		else:
			return t

	def parseStructDecl(decl, name):
		fields = []
		if "inner" in decl:
			fields = [{
				"name": field["name"],
				"type": parseType(field["type"]["qualType"])
			} for field in decl["inner"] if field["kind"] == "FieldDecl"]

		return {
			"kind": "struct",
			"name": name,
			"id": decl["id"],
			"fields": fields
		}

	def parseEnumDecl(decl, name, id):
		cases = []
		if "inner" in decl:
			cases = [{
				"name": c["name"],
				"value": parseEnumCaseValue(c["inner"]) if "inner" in c else None
			} for c in decl["inner"] if c["kind"] == "EnumConstantDecl"]

		if name == "" and infer_enum_name and len(cases) >= 2:
			tmp = cases[0]["name"]
			for i in range(len(cases) - 1):
				tmp = findCommonName(cases[i + 1]["name"], tmp)
			if tmp != "":
				name = tmp

		return {
			"kind": "enum",
			"name": name,
			"id": id,
			"cases": cases
		}

	def parseEnumCaseValue(inner):
		for child in inner:
			if child["kind"] == "FullComment":
				continue
			return parseConstantValue(child)

	def parseConstantValue(value):
		if value["kind"] == "IntegerLiteral":
			return value["value"]
		elif value["kind"] == "ConstantExpr":
			return value["value"]
			# return parseConstantValue(value["inner"][0])
		elif value["kind"] == "ImplicitCastExpr":
			return parseConstantValue(value["inner"][0])
		elif value["kind"] == "DeclRefExpr":
			return value["referencedDecl"]["name"]
		elif value["kind"] == "ParenExpr":
			return "(" + parseConstantValue(value["inner"][0]) + ")"
		elif value["kind"] == "UnaryOperator":
			if value["isPostfix"]:
				return parseConstantValue(value["inner"][0]) + value["opcode"]
			else:
				return value["opcode"] + parseConstantValue(value["inner"][0])
		elif value["kind"] == "BinaryOperator":
			return parseConstantValue(value["inner"][0]) + " " + value["opcode"] + " " + parseConstantValue(value["inner"][1])

		print("error: invalid constant expr: " + json.dumps(value, indent="\t"))
		return None

	def parseFunctionDecl(decl):
		params = []
		if "inner" in decl:
			params = [{
				"name": param["name"] if "name" in param else "_",
				"type": parseType(param["type"]["qualType"])
			} for param in decl["inner"] if param["kind"] == "ParmVarDecl"]

		return {
			"kind": "func",
			"name": decl["name"],
			"id": decl["id"],
			"return_type": parseType(decl["type"]["qualType"].split("(")[0]),
			"params": params
		}

	def parseTypedefDecl(decl, prev):
		if "inner" in decl and "ownedTagDecl" in decl["inner"][0]:
			id = decl["inner"][0]["ownedTagDecl"]["id"]
			if prev["id"] == id:
				prev["name"] = decl["name"]
				return None

		if decl["name"] in builtin_types:
			return None

		t = parseType(decl["type"]["qualType"])
		if t == decl["name"] or t.startswith("__"):
			return None

		return {
			"kind": "alias",
			"name": decl["name"],
			"id": decl["id"],
			"type": t
		}

	def parseVarDecl(decl):
		if decl["kind"] == "VarDecl":
			t = decl["type"]["qualType"]
			is_const = False
			if t.startswith("const "):
				is_const = True
				t = t[6:]

			return {
				"kind": "const" if is_const else "var",
				"name": decl["name"],
				"id": decl["id"],
				"type": parseType(t),
				"init": parseConstantValue(decl["inner"][0]) if "inner" in decl else None,
				"extern": "storageClass" in decl and decl["storageClass"] == "extern"
			}
		elif decl["kind"] == "EnumConstantDecl":
			return {
				"kind": "const",
				"name": decl["name"],
				"id": decl["id"],
				"type": "i32",
				"init": parseConstantValue(decl["inner"][0]) if "inner" in decl else None
			}
		else:
			print(decl)

	def isSystemLibrary(path):
		for d in ["/usr/lib/clang/", "/usr/include/sys", "/usr/include/bits"]:
			if path.startswith(d):
				return True
		return False

	def isLocFromSystemLibrary(loc):
		if "file" in loc and isSystemLibrary(loc["file"]):
			return True
		if "includedFrom" in loc and isSystemLibrary(loc["includedFrom"]["file"]):
			return True
		if "spellingLoc" in loc:
			return isLocFromSystemLibrary(loc["spellingLoc"])
		return False

	def parseDecl(decl, prev):
		if isLocFromSystemLibrary(decl["loc"]):
			return None

		# ignore builtin decls
		if "name" in decl and (decl["name"].startswith("__") or decl["name"] in builtin_types):
			return None

		match decl["kind"]:
			case "RecordDecl":
				if "name" in decl:
					return parseStructDecl(decl, decl["name"])
				else:
					return None
			case "EnumDecl":
				if "name" in decl:
					return parseEnumDecl(decl, decl["name"], decl["id"])
				else:
					return parseEnumDecl(decl, "", decl["id"])
			case "FunctionDecl":
				return parseFunctionDecl(decl)
			case "TypedefDecl":
				return parseTypedefDecl(decl, prev)
			case "VarDecl":
				return parseVarDecl(decl)
			case _:
				return None

	def findCommonPrefix(a, b):
		i = 0
		while i < min(len(a), len(b)):
			if a[:i] != b[:i]:
				if i == 0:
					return ""
				return a[:(i-1)]
			i += 1
		return a[:i]

	def findCommonPostfix(a, b):
		i = 1
		while i < min(len(a), len(b)) + 1:
			if a[-i:] != b[-i:]:
				if i == 0:
					return ""
				return a[-(i-1):]
			i += 1
		return a[-i:]

	def findCommonName(a, b):
		prefix = findCommonPrefix(a, b)
		# if pascal case and last char is upper cut it off
		if len(prefix) >= 2 and prefix[-1].isupper() and prefix[-2].islower():
			prefix = prefix[:-1]

		postfix = findCommonPostfix(a, b)
		# if Pascal case and begin is lowercase cut it off
		if len(postfix) >= 2:
			i = 0
			while i < len(postfix) - 2:
				if postfix[i].islower() and postfix[i + 1].isupper():
					postfix = postfix[i+1:]
				elif postfix[i].isupper():
					break
				i += 1

		if prefix.endswith(postfix):
			return prefix
		elif postfix.startswith(prefix):
			return postfix
		else:
			return prefix + postfix

	ast = clang(args[1])
	decls = []
	unique_decls = set()
	for decl in ast:
		d = parseDecl(decl, decls[-1] if len(decls) > 0 else None)
		if d is None or d["name"] in unique_decls:
			continue

		decls.append(d)
		unique_decls.add(d["name"])

	output = "import std/core;\n"

	prev_kind = ""
	for decl in decls:
		match decl["kind"]:
			case "struct":
				output += "\nstruct " + decl["name"] + " {"
				if len(decl["fields"]) > 0:
					output += "\n"

				for v in decl["fields"]:
					output += "\tvar " + v["name"] + ": " + v["type"] + ";\n"

				if generate_default_functions and len(decl["fields"]) > 0:
					output += "\n"
					output += "\tfunc constructor(this: &&" + decl["name"] + ", other: " + decl["name"] + ") -> void = default;\n"
					output += "\tfunc destructor(this: &&" + decl["name"] + ") -> void = default;\n"
					output += "\toperator =(this: &&" + decl["name"] + ", other: " + decl["name"] + ") -> void = default;\n"
					output += "\toperator ==(this: " + decl["name"] + ", other: " + decl["name"] + ") -> bool = default;\n"

				output += "}\n"
			case "enum":
				if decl["name"] == "" or decl["name"].startswith("0x"): # anonymous enum
					output += "\n"
					next_id = 0
					for c in decl["cases"]:
						output += "comptime const " + c["name"]
						if "value" in c and not c["value"] is None:
							next_id = int(c["value"])
							output += " = " + c["value"]
						else:
							output += " = " + str(next_id)
						next_id += 1
						output += ";\n"
				else:
					output += "\nenum " + decl["name"] + " {"
					if len(decl["cases"]) > 0:
						output += "\n"

					for c in decl["cases"]:
						output += "\tcase " + c["name"]
						if "value" in c and not c["value"] is None:
							output += " = " + c["value"]
						output += ";\n"

					if generate_default_functions:
						output += "\n"
						output += "\toperator &(this: " + decl["name"] + ", other: " + decl["name"] + ") -> " + decl["name"] + " = default;\n"
						output += "\toperator |(this: " + decl["name"] + ", other: " + decl["name"] + ") -> " + decl["name"] + " = default;\n"

					output += "}\n"
			case "alias":
				if prev_kind != decl["kind"]:
					output += "\n"
				output += "alias " + decl["name"] + " = " + decl["type"] + ";\n"
			case "const" | "var":
				if not allow_global_variables:
					print("error: global variables aren't allowed, but needed for: " + json.dumps(decl, indent="\t"))
					continue
				if prev_kind != decl["kind"]:
					output += "\n"
				output += decl["kind"] + " " + decl["name"]
				if "type" in decl and not decl["type"] is None:
					output += ": " + decl["type"]
				if decl["extern"]:
					output += " = extern"
				elif "init" in decl and not decl["init"] is None:
					output += " = " + decl["init"]
				output += ";\n"
			case "func":
				if prev_kind != decl["kind"]:
					output += "\n"
				output += "func " + decl["name"] + "("
				output += ", ".join(param["name"] + ": " + param["type"] for param in decl["params"])
				output += ") -> " + decl["return_type"] + " = extern;\n"

		prev_kind = decl["kind"]

	if dst == "--":
		print(output)
	else:
		with open(dst, "w") as f:
			f.write(output)

if __name__ == "__main__":
	main(sys.argv)
