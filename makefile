# llvm libraries:
# llvm-config --libs --link-static core analysis target bitwriter
# llvm also depends on libncurses (terminal io) and libz (compression)

build/compiler: src/*.jakt
	@~/.local/jakt/bin/jakt -J16 src/compiler.jakt -O -lncurses -lzstd -lz -lLLVM

test:
	@./test.py -- -r -bc -s

clean:
	@rm build/*
