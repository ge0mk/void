"alias" @keyword
"as" @keyword
"break" @keyword
"case" @keyword
"comptime" @keyword
"const" @keyword
"continue" @keyword
"default" @keyword
"defer" @keyword
"discard" @keyword
"do" @keyword
"else" @keyword
"enum" @keyword
"extern" @keyword
"false" @keyword
"for" @keyword
"func" @keyword
"if" @keyword
"import" @keyword
"in" @keyword
"is" @keyword
"match" @keyword
"must" @keyword
"namespace" @keyword
"operator" @keyword
"pragma" @keyword
"private" @keyword
"return" @keyword
"struct" @keyword
"template" @keyword
"throw" @keyword
"true" @keyword
"try" @keyword
"var" @keyword
"variant" @keyword
"while" @keyword
"yield" @keyword

"." @delimiter
";" @delimiter

"true" @constant
"false" @constant

(function_decl (identifier) @function)
(type_decl (identifier) @type)

(import_stmt (identifier) @string)

(type (name)) @type

(parameter_decl (identifier) @variable.parameter)
(var_decl (identifier) @variable)

(variant_case_decl (identifier) @constant)

(bin_literal) @number
(oct_literal) @number
(dec_literal) @number
(hex_literal) @number
(char_literal) @string
(string_literal) @string

(comment) @comment
