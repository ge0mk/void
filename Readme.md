void - language & compiler
==

dependencies
--
- llvm >= 15.0 (binaries, headers & clang)

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
- compiler: namespaces
	- every module & type has a namespace
	- functions & types are inside of namespaces (not module / parent-type)
	- -> faster symbol lookup
	- public / private namespaces, types & functions
- typechecker: track member (de)initialization through if & match stmts
- codegen: generate better llvm ir
	- function attributes (especially for allocators)
- codegen: better debug info
- typechecker: high-level optimizations:
	- for x in NumericRange -> builtin count-for-loop
	- function inlining
- typechecker+parser: function references
- typechecker+parser: anonymous functions
- compiler: performance optimizations
	- do less unneccessary stuff
	- multithreading (at least typechecking of function bodies)
- compiler: builtin vector types for faster math
- meta:
	- lsp interface
- stdlib: some clean-up:
	- merge VRange & Range, make is_const a template parameter
	- reduce duplicated code in Optional & Result with updated comptime if syntax
- typechecker+parser: optional chaining `foo()?.bar()`
	- `bar()` can be any operator, function call or member var access
	- codegen to `foo().value().bar() if foo().hasValue() else None` (but only codegen `foo()` once)
	- if `bar()` doesn't yield `Optional!<T>`, wrap it in `Some()`
	- also for `Result!<T, E>`
		- result from `foo()` and `bar()` must have the same error type or `bar()` must not yield a result type
- typechecker: template parameter inferance ?
- typechecker: variadic templates
	- compiletime for-each to iterate parameters
- typechecker+interpreter: expand compile time code execution (ast interpreter)
	- provide functions to query system info at compile-time (e.g. os, architecture, ...)
	- extend reflection library (get information about types at compile-time)
	- make all builtin functions & libc external functions available at compile time
- typechecker: traits / concepts to restrict types accepted by template parameters
- typechecker: tuples
- typechecker: tuple unpacking / destructuring assignments
- typechecker: match strings
- typechecker: unsafe functions, which can only be called in unsafe blocks
- typechecker: type aliases
- typechecker: pick const / non-const functions depending on the usage of the result value
- typechecker: defer statements
- typechecker: better error messages for const / non-const conflicts:
	"no matching function found" -> "can't call mutating function on const object"
- typechecker: arithmetic expressions as template parameters
- typechecker: enums as template parameters
- compiler: incremental builds / cashing of (partially) compiled modules (llvm-ir, output of typechecker ?)
- stdlib:
	- `format("{}", ...)` for text formatting, similar to https://github.com/fmtlib/fmt
		- requires variadic templates, better comptime code execution & traits
	- `embed<T>()` to include files at compile-time as array/string constants

planned features (far future)
--
- compile to spirv -> shaders written in void
- don't depend on libc / compiler_rt ?
- built-in ui markup language (like qml)
