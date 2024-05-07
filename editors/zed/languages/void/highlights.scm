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

(template_parameter (identifier) @type)
(function_decl (identifier) @function)
(function_decl (operator_name) @function)
(type_decl (identifier) @type)

(import_stmt (identifier) @string)

(type (operand (name (identifier) @type)))
(name (operand (name (identifier) @type)))
(named_tuple_expr (identifier) @property)

(parameter_decl (identifier) @variable.parameter)
(var_decl (identifier) @variable)
(type_decl (compound_stmt (var_decl (identifier) @property)))
(for_stmt (identifier) @variable)

(variant_case_decl (identifier) @constant)
(match_case_decl (operand (name (identifier) @constant)))

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

(call_expr callee: (operand
	(name (identifier) @function)
))

(operand
	(member_access_expr rhs: (operand
		(name (identifier) @property)
	))
)

(call_expr callee: (operand
	(member_access_expr rhs: (operand
		(name (identifier) @function)
	))
))

(operand
	(namespace_expr (operand
		(name (identifier) @type)
	))
)

(call_expr callee: (operand
	(namespace_expr rhs: (operand
		(name (identifier) @function)
	))
))

(comment) @comment
