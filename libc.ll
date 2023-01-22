; ModuleID = 'main.ll'
source_filename = "main"
target triple = "x86_64-pc-linux-gnu"

@stdin = external global ptr, align 8
@stdout = external global ptr, align 8
@stderr = external global ptr, align 8

declare ptr @__errno_location()

define ptr @"get_errno"() {
entry:
  %0 = call ptr @__errno_location()
  ret ptr %0
}

define ptr @"std::libc::stdin"() {
entry:
  %0 = load ptr, ptr @stdin, align 8
  ret ptr %0
}

define ptr @"std::libc::stdout"() {
entry:
  %0 = load ptr, ptr @stdout, align 8
  ret ptr %0
}

define ptr @"std::libc::stderr"() {
entry:
  %0 = load ptr, ptr @stderr, align 8
  ret ptr %0
}
