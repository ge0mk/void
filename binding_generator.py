#!/usr/bin/python3

import json
import subprocess
import sys

builtin_types = {
	"void": "void",

	"int8_t": "i8",
	"int16_t": "i16",
	"int32_t": "i32",
	"int64_t": "i64",

	"uint8_t": "u8",
	"uint16_t": "u16",
	"uint32_t": "u32",
	"uint64_t": "u64",

	"size_t": "uint",
	"intptr_t": "int",
	"uintptr_t": "uint",
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
	"long long": "i32",
	"unsigned long long": "u32",

	"float": "f32",
	"double": "f64",
}

def getParseFile(path):
	cmd = ['clang', '-Xclang', '-ast-dump=json', '-c', path]

	ast = json.loads(subprocess.check_output(cmd))
	decls = {}

	for elem in ast["inner"]:
		if elem["loc"] == {}:
			continue

		if not "name" in elem:
			elem["name"] = elem["id"]

		if elem["name"][0:2] == "__":
			continue

		if "includedFrom" in elem["loc"]:
			path = elem["loc"]["includedFrom"]["file"]
			if path.startswith("/usr/lib/clang/"):
				continue
			if path.startswith("/usr/include/sys"):
				continue

		del elem["id"]
		del elem["loc"]
		del elem["range"]

		if elem["kind"] == "TypedefDecl":
			if elem["name"] in builtin_types:
				elem = {
					"name": elem["name"],
					"kind": "BuiltinType",
					"type": builtin_types[elem["name"]]
				}
			elif "qualType" in elem["type"] and elem["type"]["qualType"] in builtin_types:
				elem = {
					"name": elem["name"],
					"kind": "BuiltinType",
					"type": builtin_types[elem["type"]["qualType"]]
				}
			elif "desugaredQualType" in elem["type"] and elem["type"]["desugaredQualType"] in builtin_types:
				elem = {
					"name": elem["name"],
					"kind": "BuiltinType",
					"type": builtin_types[elem["type"]["desugaredQualType"]]
				}
			elif elem["name"].endswith("_t"):
				# "Names that end with ‘_t’ are reserved for additional type names. "
				# -> ignore all types ending in _t that have no equivalent
				continue

		decls[elem["name"]] = elem

	return decls

def main(args):
	src = args[1]
	dst = args[2]

	ast = getParseFile(src)

	type_decls = {}
	type_aliases = {}
	function_decls = {}

	def parse_type(t):
		t = t.strip().replace("struct ", "").replace("enum ", "")

		if t in builtin_types:
			return builtin_types[t]
		elif t in type_aliases:
			return type_aliases[t]
		elif t[-1] == '*':
			if t.startswith("const "):
				return "cptr!<" + parse_type(t[6:-1]) + ">"
			else:
				return "vptr!<" + parse_type(t[:-1]) + ">"
		else:
			print("unknown type: " + t)

	for name, decl in ast.items():
		match decl["kind"]:
			case "BuiltinType":
				type_aliases[name] = decl["type"]
			case "RecordDecl":
				type_aliases[name] = name
				type_decls[name] = {
					"kind": "struct",
					"member_variables": []
				}
			case "EnumDecl":
				cases = []
				for c in decl["inner"]:
					if c["kind"] != "EnumConstantDecl":
						continue
					case_name = c["name"]
					id = None
					if "inner" in c:
						tmp = c["inner"][0]
						if tmp["kind"] == "ConstantExpr":
							id = tmp["value"]
					cases.append((case_name, id))
				type_aliases[name] = name
				type_decls[name] = {
					"kind": "enum",
					"cases": cases
				}
			case "TypedefDecl":
				pass

	for name, decl in ast.items():
		if decl["kind"] != "TypedefDecl":
			continue

		if "ownedTagDecl" in decl["inner"][0]:
			id = decl["inner"][0]["ownedTagDecl"]["id"]
			if id in type_decls:
				type_decls[name] = type_decls[id]
				type_aliases[name] = name
				del type_decls[id]
				del type_aliases[id]

	for name, decl in ast.items():
		if decl["kind"] != "TypedefDecl":
			continue

		qual_type = decl["type"]["desugaredQualType"] if "desugaredQualType" in decl["type"] else decl["type"]["qualType"]
		type = parse_type(qual_type)
		if not type is None:
			type_aliases[name] = type

	for name, decl in ast.items():
		if decl["kind"] != "FunctionDecl":
			continue

		return_type = parse_type(decl["type"]["qualType"].split("(")[0])
		if return_type is None:
			continue

		parameters = []
		if "inner" in decl:
			for child in decl["inner"]:
				if child["kind"] != "ParmVarDecl":
					continue
				param_name = child["name"] if "name" in child else "_"

				type = parse_type(child["type"]["qualType"])

				if type is None:
					parameters = None
					break

				param = (param_name, type)
				parameters.append(param)

		if parameters is None:
			continue

		function_decls[name] = {
			"parameters": parameters,
			"return_type": return_type
		}

	output = "import std/core;\n\n"

	for name, decl in type_decls.items():
		if name.startswith("0x"):
			continue

		match decl["kind"]:
			case "struct":
				output += "struct " + name + " {"
				member_variables = decl["member_variables"]
				if member_variables == []:
					output += "}"
				else:
					pass
			case "enum":
				output += "enum " + name + " {"
				cases = decl["cases"]
				if cases == []:
					output += "}"
				else:
					output += "\n"
					for name, id in cases:
						output += "\tcase " + name
						if not id is None:
							output += " = " + id
						output += ";\n"
					output += "}"
		output += "\n\n"

	for name, func in function_decls.items():
		output += "extern func " + name + "("
		output += ", ".join(param[0] + ": " + param[1] for param in func["parameters"])
		output += ") -> " + func["return_type"] + ";\n"

	with open(dst, "w") as f:
		f.write(output)

if __name__ == "__main__":
	main(sys.argv)
