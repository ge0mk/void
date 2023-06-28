main: stage1

clean:
	-@rm build/*

clean-but-keep-stage0:
	-@find build ! -name 'stage0' -type f -exec rm -f {} +

build/void: build/stage1
	-@cp -u build/stage1 build/void

stage0: build/stage0

bootstrap.ll:
	wget -O bootstrap.ll https://github.com/ge0mk/void/releases/download/selfhosted/bootstrap.ll

build/stage0: bootstrap.ll
	clang bootstrap.ll -o build/stage0 -lc -lm -lLLVM

test-stage0: build/stage0
	python3 test.py build/stage0 -q -- -r -bc -s

stage1: build/stage1

build/stage1: build/stage1.ll
	clang build/stage1.ll -o build/stage1 -lc -lm -lLLVM

build/stage1.ll: build/stage0 std/*.vd src/*.vd src/*/*.vd
	build/stage0 src/main.vd -o stage1 -c -g -m

test-stage1: build/stage1
	python3 test.py build/stage1 -q -- -m -b -s

stage2: build/stage2

build/stage2: build/stage2.ll
	clang build/stage2.ll -o build/stage2 -lc -lm -lLLVM

build/stage2.ll: build/stage1 std/*.vd src/*.vd src/*/*.vd llvm/*.vd
	build/stage1 src/main.vd -o stage2 -c -g -m

test-stage2: build/stage2
	python3 test.py build/stage2 -q -- -m -b -s

llvm/llvm_c.vd: llvm/llvm.h
	python3 binding_generator.py llvm/llvm.h llvm/llvm_c.vd

libc.ll: libc.c
	clang libc.c -S -emit-llvm -O3 -o libc.ll

generate-bootstrap-files: build/stage2
	build/stage2 src/main.vd -o bootstrap -c -m
	build/stage2 src/main.vd -o bootstrap-bc -c -m -b
	build/stage2 src/main.vd -o bootstrap-stripped -c -m -s
	build/stage2 src/main.vd -o bootstrap-stripped-bc -c -m -s -b

	-@cp -f build/bootstrap* bootstrap/

# llvm libraries:
# llvm-config --libs --link-static core analysis target bitwriter
# llvm also depends on libncurses (terminal io) and libz (compression)
