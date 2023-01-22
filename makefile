# llvm libraries:
# llvm-config --libs --link-static core analysis target bitwriter
# llvm also depends on libncurses (terminal io) and libz (compression)

build/compiler: src/*.jakt
	@~/.local/jakt/bin/jakt -J16 src/compiler.jakt -O -lncurses -lzstd -lz \
		-lLLVMIRReader -lLLVMAsmParser -lLLVMLinker -lLLVMTransformUtils -lLLVMBitWriter -lLLVMTarget -lLLVMAnalysis -lLLVMProfileData -lLLVMSymbolize -lLLVMDebugInfoPDB -lLLVMDebugInfoMSF -lLLVMDebugInfoDWARF -lLLVMObject -lLLVMTextAPI -lLLVMMCParser -lLLVMMC -lLLVMDebugInfoCodeView -lLLVMBitReader -lLLVMCore -lLLVMRemarks -lLLVMBitstreamReader -lLLVMBinaryFormat -lLLVMSupport -lLLVMDemangle \

test:
	@./test.py -- -r -bc -s

clean:
	@rm build/*
