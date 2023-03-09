TODO until feature parity with jakt based compiler:
==
- fix bugs

Typechecker:
==

1) check top-level stmts
	- import -> import module
	- comptime stmt -> interpret
		- requires that all imported modules are fully checked
	- function-decl
		- check template parameters
		- add to list of unchecked functions
	- type-decl
		- check template parameters
		- add type to its parent module

2) check type implementations
	- all types of the current module & imports must have been checked previously
	- when all template parameters are specified:
		- check child stmts
			- comptime stmt -> interpret
			- function-decl
				- check template parameters
				- add to list of unchecked functions
			- var or case decl -> add to type members
		- add builtin functions (e.g. variant constructors) to list of unchecked-functions

3) check function definitions
	- check template parameters
	- add function to its parent module
	- when all template parameters are specified:
		- check signature
		- add body to list of unchecked function bodies

4) check function implementations

5) done

-> Typechecker context = statemachine
- store typechecking context inside module
- when instantiating a template typecheck it immediately with it's parent modules typechecking context, complete all steps < the current modules step
- when advancing to the next step make sure all imported modules are at a later step
-> recursive, bad for multithreading but easy to implement


Interpreter:
==

1) typecheck expressions
	- if a called function isn't already checked, check it immediately
2) codegen expression & cleanup into a function each
	- result & temporaries get stored in preallocated memory
	- pointers can be hardcoded as literals
3) interpret expression function `LLVMRunFunction()`
4) convert result into usable format for typechecker
	- only works for selected types
5) interpret cleanup function `LLVMRunFunction()`
6) interpret statements based on result / use result as constant expr
	- e.g. if stmt: check body based on result

``
LLVMBool LLVMCreateInterpreterForModule(LLVMExecutionEngineRef *OutInterp, LLVMModuleRef M, char **OutError);
LLVMGenericValueRef LLVMRunFunction(LLVMExecutionEngineRef EE, LLVMValueRef F, unsigned NumArgs, LLVMGenericValueRef *Args);
``

- reflection library has full access to compiler code & memory at runtime
	- self modifying code at compile-time
	- language can be extended without recompiling the compiler

syntax sugar replacements:
==

// if-var
if var x = y {
	z()
}
->
match y {
	Ok: x -> {
		z()
	}
}

// var-else
var x = y else {
	z()
}
->
var x = match y {
	Ok: x -> yield x;
	else -> {
		z()
	}
}

// try
try foo()
->
match foo() {
	Ok: val -> yield val;
	Error: err -> throw err;
}

// must
must foo()
->
match foo() {
	Ok: val -> yield val;
	Error: err -> panic(err);
}

// variant op safe as
x as Foo
->
match x {
	case Foo: val -> yield Some(val);
	else -> yield None;
}

// inline if
x if y else z
->
match y {
	true -> yield x;
	else -> yield z;
}

// for loop
for (&&)value in range() {
	...
}
->
{
	var range = range();
	var iterator = range.iterator();
	while iterator.hasNext() {
		var value = (&&)iterator.next();
		...
	}
}




when selfhosted compiler works:
--
- clean-up standard library:
	- merge VRange & Range, make is_const a template parameter
	- reduce duplicated code in Optional & Result with updated comptime if syntax
	- remove outdated iterator interface (next() -> Optional)
	- ...
- refactor compiler to make use of match expressions for better readability in some places:
	- ...
- implement some high-level optimizations:
	- for x in NumericRange -> builtin count-for-loop
	- remove unnecesary copies
