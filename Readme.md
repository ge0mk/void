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
func main() -> void {
	println("Hello world!");
}
```

planned features (wip / near future)
--
- typechecker: track member (de)initialization through match stmts
- codegen: generate better llvm ir
	- function attributes (especially for allocators)
- codegen: better debug info
- typechecker: high-level optimizations:
	- function inlining
- compiler: multithreading
- compiler: builtin vector types for faster math
- typechecker: traits / concepts to restrict types accepted by template parameters
- typechecker: enums / variant cases as template parameters
- typechecker: variadic templates
	- compiletime for-each to iterate parameters
- typechecker: template parameter inferance ?
- typechecker+interpreter: expand compile time code execution (ast interpreter)
	- implement comptime if-var, var-else & for statements, comptime match statement ?
	- provide functions to query system info at compile-time (e.g. os, architecture, ...)
	- extend reflection library (get information about types at compile-time)
	- make all builtin functions & libc external functions available at compile time
- stdlib:
	- `format("{}", ...)` for text formatting, similar to https://github.com/fmtlib/fmt
		- requires variadic templates, better comptime code execution & traits
	- `embed<T>()` to include files at compile-time as array/string constants
	- threads
	- tcp / udp sockets
- compiler:
	- lsp interface
- typechecker+parser: optional chaining `foo()?.bar()`
	- `bar()` can be any operator, function call or member var access
	- codegen to `foo().value().bar() if foo().hasValue() else None` (but only codegen `foo()` once)
	- if `bar()` doesn't yield `Optional!<T>`, wrap it in `Some()`
	- also for `Result!<T, E>`
		- result from `foo()` and `bar()` must have the same error type or `bar()` must not yield a result type
- typechecker: tuple unpacking / destructuring assignments
- typechecker: generic match for non-integer types (e.g. String)
- typechecker: pick const / non-const functions depending on the usage of the result value
- typechecker: better error messages for const / non-const conflicts:
	"no matching function found" -> "can't call mutating function on const object"
- compiler: incremental builds / cashing of (partially) compiled modules (llvm-ir, output of typechecker ?)
- compiler: public / private namespaces, types & functions

planned features (far future)
--
- compile to spirv -> shaders written in void
- don't depend on libc / compiler_rt ?
- built-in ui markup language (like qml)
