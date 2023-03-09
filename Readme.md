void - language & compiler
==

build the compiler
--
```bash
git clone https://github.com/ge0mk/void
cd void
make
```

hello world
--
```
import std/core;
import std/string;
import std/io;
func main() {
	println("Hello world!");
}
```

planned features (wip / near future)
--
- meta: write a better readme
- compiler: generate better llvm ir
	- lifetime intrinsics
	- function attributes (especially for allocators)
- compiler: optional chaining `foo()?.bar()`
	- `bar()` can be any operator, function call or member var access
	- codegen to `foo().value().bar() if foo().hasValue() else None` (but only codegen `foo()` once)
	- if `bar()` doesn't yield `Optional!<T>`, wrap it in `Some()`
	- also for `Result!<T, E>`
		- result from `foo()` and `bar()` must have the same error type or `bar()` must not yield a result type
- compiler: template parameter inferance ?
- compiler: variadic templates
	- compiletime for-each to iterate parameters
- compiler: expand compile time code execution (ast interpreter)
	- provide functions to query system info at compile-time (e.g. os, architecture, ...)
	- extend reflection library (get information about types at compile-time)
	- make all builtin functions & libc external functions available at compile time
- compiler: traits / concepts to restrict types accepted by template parameters
- compiler: tuples
- compiler: tuple unpacking / destructuring assignments
- compiler: match strings
- compiler: track member (de)initialization through if & match stmts
- compiler: unsafe functions, which can only be called in unsafe blocks
- compiler: public / private functions (module scope) & member variables
- compiler: type aliases
- compiler: pick const / non-const functions depending on the usage of the result value
- compiler: defer statements
- compiler: better error messages for const / non-const conflicts:
	"no matching function found" -> "can't call mutating function on const object"
- compiler: arithmetic expressions as template parameters
- compiler: enums as template parameters
- compiler: function references
- compiler: anonymous functions
- compiler: better debug info
	- types
	- variables
- compiler: optimizations on ast-level:
	- eliminate unnecessary copying
	- function inlining
- compiler: cashing of (partially) compiled modules (llvm-ir, output of typechecker ?)
- stdlib:
	- `format("{}", ...)` for text formatting, similar to https://github.com/fmtlib/fmt
		- requires variadic templates, better comptime code execution & traits
	- `embed<T>()` to include files at compile-time as array/string constants
- meta:
	- lsp interface

planned features (far future)
--
- compile to spirv -> shaders written in void
- don't depend on libc / compiler_rt ?
- built-in ui markup language (like qml)
