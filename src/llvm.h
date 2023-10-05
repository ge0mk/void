// used to generate the llvm binding
// put all required llvm headers here and run `./binding_generator.py selfhost/llvm.h selfhost/llvm.vd` to generate selfhost/llvm.vd

#include <llvm-c/Types.h>
#include <llvm-c/Core.h>
#include <llvm-c/ErrorHandling.h>
#include <llvm-c/Initialization.h>
#include <llvm-c/Analysis.h>
#include <llvm-c/Target.h>
#include <llvm-c/IRReader.h>
#include <llvm-c/BitReader.h>
#include <llvm-c/BitWriter.h>
#include <llvm-c/Linker.h>
#include <llvm-c/DebugInfo.h>
#include <llvm-c/ExecutionEngine.h>
