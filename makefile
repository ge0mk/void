# llvm libraries:
# llvm-config --libs --link-static core analysis target bitwriter
# llvm also depends on libncurses (terminal io) and libz (compression)

build/compiler: src/*.jakt libc.ll
	@~/.local/jakt/bin/jakt -J16 src/compiler.jakt -O -lncurses -lzstd -lz -lLLVM

libc.ll: libc.c
	@clang libc.c -S -emit-llvm -O3 -o libc.ll

test:
	@./test.py -- -r -bc -s

clean:
	@rm build/*
