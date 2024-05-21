[
	"alias"
	"break"
	"case"
	"comptime"
	"const"
	"continue"
	"default"
	"defer"
	"discard"
	"do"
	"else"
	"enum"
	"extern"
	"false"
	"for"
	"func"
	"if"
	"import"
	"in"
	"match"
	"must"
	"namespace"
	"operator"
	"pragma"
	"private"
	"return"
	"struct"
	"template"
	"throw"
	"true"
	"try"
	"var"
	"variant"
	"while"
	"yield"
] @keyword

[ "::" ":" "." "," ";" "->" ] @punctuation.delimiter

[ "(" ")" "[" "]" "{" "}" ] @punctuation.bracket

[
	"&" "|" "^" "~" "<<" ">>"
	"+" "-" "*" "/" "%"
	"++" "--"
	".."
	"=" ":="
	"&=" "|=" "^=" "~=" "<<=" ">>="
	"+=" "-=" "*=" "/=" "%="
	"==" "!=" "<" "<=" ">" ">=" "<=>"
	"||" "&&" "!"
	"as" "is"
] @operator

["true" "false"] @constant.builtin

(name "<" @punctuation.bracket ">" @punctuation.bracket)

(import (identifier) @string)

(template_parameter (identifier) @type)
(function_decl (identifier) @function)
(function_decl (operator_name) @function)
(struct_decl (identifier) @type)
(enum_decl (identifier) @type)
(variant_decl (identifier) @type)
(namespace_decl (identifier) @type)
(type_alias (identifier) @type)

(type (name (identifier) @type))
(type (prefix_expr (name (identifier) @type)))
(name (name (identifier) @type))
(named_tuple_element (identifier) @property)

(parameter_decl (identifier) @variable.parameter)
(var_decl (identifier) @variable)
(for_stmt (identifier) @variable)

(variant_case_decl (identifier) @constant)
(match_case_decl (name (identifier) @constant))

[
	(bin_literal)
	(oct_literal)
	(dec_literal)
	(hex_literal)
] @number

(char_literal) @string.quoted.double
(string_literal) @string.quoted.single
(escape_sequence) @escape

(bin_literal (identifier) @type)
(oct_literal (identifier) @type)
(dec_literal (identifier) @type)
(hex_literal (identifier) @type)
(char_literal (identifier) @type)
(string_literal (identifier) @type)

(call_expr callee: (name (identifier) @function))
(member_access_expr rhs: (name (identifier) @property))
(call_expr callee: (member_access_expr rhs: (name (identifier) @function)))
(namespace_expr (name (identifier) @type))
(call_expr callee: (namespace_expr rhs: (name (identifier) @function)))

(comment) @comment
