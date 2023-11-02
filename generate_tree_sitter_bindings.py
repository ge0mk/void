import os, subprocess, sys
from tree_sitter import Language, Parser

subprocess.run([
	"python3",
	"binding_generator.py",
	"src/tree_sitter.h",
	"src/tree_sitter.vd",
	"--generate-struct-default-constructor=TSNode",
	"--generate-struct-copy-constructor",
	"--generate-struct-destructor",
	"--generate-struct-op-assign",
	"--generate-struct-op-equal",
], check=True)

subprocess.run(["python3", "setup.py", "build"], cwd="./tree-sitter-void/", check=True)
sys.path.append(os.path.abspath("./tree-sitter-void/build/lib.linux-x86_64-cpython-312/"))

import tree_sitter_void

lang = Language(tree_sitter_void.language())

with open("src/tree_sitter.vd", "a") as o:
	o.write("\nenum TSVoidSymbol : u16 {\n")
	for id in range(lang.node_kind_count + 1):
		name = lang.node_kind_for_id(id)
		if name is None:
			continue

		if lang.node_kind_is_named(id):
			name = name.replace("_", " ").title().replace(" ", "")
			o.write(f"\tcase {name} = {id};\n")
		elif name.isalpha() and name.islower():
			name = "Keyword" + name.title()
			o.write(f"\tcase {name} = {id};\n")
	o.write("}\n")

	o.write("\nenum TSVoidField : u16 {\n")
	for id in range(lang.field_count + 1):
		name = lang.field_name_for_id(id)
		if name is None:
			continue
		name = name.replace("_", " ").title().replace(" ", "")
		o.write(f"\tcase {name} = {id};\n")
	o.write("}\n")
