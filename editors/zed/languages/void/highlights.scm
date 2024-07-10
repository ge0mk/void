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

[ "::" ":" "." "," ";" "->" "=>" ] @punctuation.delimiter

[ "(" ")" "[" "]" "{" "}" ] @punctuation.bracket

[
	"&" "|" "^" "~" "<<" ">>"
	"+" "-" "*" "/" "%"
	"++" "--"
	".."
	"=" ":="
	"&=" "|=" "^=" "<<=" ">>="
	"+=" "-=" "*=" "/=" "%="
	"==" "!=" "<" "<=" ">" ">=" "<=>"
	"||" "&&" "!"
	"as" "is"
] @operator

(name "<" @punctuation.bracket ">" @punctuation.bracket)

(import (identifier) @string)

(name (identifier) @variable)

(template_parameter (identifier) @type)
(function_decl (identifier) @function)
(function_decl (operator_name) @function)
(struct_decl (identifier) @type)
(enum_decl (identifier) @type)
(variant_decl (identifier) @type)
(namespace_decl (identifier) @type)
(type_alias (identifier) @type)

(named_tuple_element (identifier) @property)

(parameter_decl (identifier) @variable.parameter)
(var_decl (identifier) @variable)
(if_var_stmt (identifier) @variable)
(var_else_stmt (identifier) @variable)
(for_stmt (identifier) @variable)

(variant_case_decl (identifier) @constant)
(match_case_decl (name (identifier) @constant))

(bool_literal) @constant.builtin
(number_literal) @number
(char_literal) @string.quoted.double
(string_literal) @string.quoted.single
(escape_sequence) @escape

(literal (identifier) @type)

(call_expr callee: (name (identifier) @function))
(member_access_expr rhs: (name (identifier) @property))
(call_expr callee: (member_access_expr rhs: (name (identifier) @function)))
(call_expr callee: (namespace_expr rhs: (name (identifier) @function)))

(attribute name: _ @string)

(comment) @comment
