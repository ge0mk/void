main: stage1

test: test-stage1

clean:
	-@rm -rf build
	-@rm -rf bootstrap
	-@rm -f rt.ll
	-@rm -f llvm/llvm_c.vd

clean-but-keep-stage0:
	-@find build ! -name 'stage0*' -type f -exec rm -rf {} +
	-@rm -rf bootstrap
	-@rm -f rt.ll
	-@rm -f llvm/llvm_c.vd

stage0: build/stage0

build/stage0: build/stage0.ll
	clang build/stage0.ll -o build/stage0 -lc -lm -lLLVM -ltcmalloc -O3 -march=native -flto

build/stage0.ll:
	-@mkdir build -p
	wget -O build/stage0.ll https://github.com/ge0mk/void/releases/latest/download/bootstrap.ll

test-stage0: build/stage0
	python3 test.py build/stage0 -q -- -m -b -s

stage1: build/stage1

build/stage1: build/stage1.ll
	clang build/stage1.ll -o build/stage1 -lc -lm -lLLVM

build/stage1.ll: build/stage0 rt.ll std/*.vd src/*.vd src/llvm_c.vd
	build/stage0 src/main.vd -o stage1 -c -g -m

test-stage1: build/stage1
	python3 test.py build/stage1 -q -- -m -b -s

stage2: build/stage2

build/stage2: build/stage2.ll
	clang build/stage2.ll -o build/stage2 -lc -lm -lLLVM

build/stage2.ll: build/stage1
	build/stage1 src/main.vd -o stage2 -c -g -m

test-stage2: build/stage2
	python3 test.py build/stage2 -q -- -m -b -s

src/llvm_c.vd: src/llvm.h
	python3 binding_generator.py src/llvm.h src/llvm_c.vd

rt.ll: rt.c
	clang rt.c -S -emit-llvm -O3 -o rt.ll

generate-bootstrap-files: build/stage2
	build/stage2 src/main.vd -o bootstrap -c -m -O
	build/stage2 src/main.vd -o bootstrap -c -m -O -b
	build/stage2 src/main.vd -o bootstrap-stripped -c -m -O -s
	build/stage2 src/main.vd -o bootstrap-stripped -c -m -O -s -b

	-@mkdir bootstrap -p
	-@cp -f build/bootstrap* bootstrap/

update-stage0:
	-@$(MAKE) --no-print-directory generate-bootstrap-files
	-@cp -f build/bootstrap.ll build/stage0.ll
	-@$(MAKE) --no-print-directory stage0

.PHONY: \
	main test \
	clean clean-but-keep-stage0 \
	stage0 test-stage0 \
	stage1 test-stage1 \
	stage2 test-stage2 \
	generate-bootstrap-files update-stage0

# llvm libraries:
# llvm-config --libs --link-static core analysis target bitwriter
# llvm also depends on libncurses (terminal io) and libz (compression)
