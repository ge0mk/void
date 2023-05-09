; ModuleID = 'main.ll'
source_filename = "main"
target triple = "x86_64-pc-linux-gnu"

@stdin = external global ptr, align 8
@stdout = external global ptr, align 8
@stderr = external global ptr, align 8

@panic_msg = private unnamed_addr constant [17 x i8] c"(internal error) ", align 1

define void @panic_errno(i32 %0) {
  %2 = call ptr @strerror(i32 %0)
  %3 = load ptr, ptr @stderr, align 8
  %4 = call i64 @fwrite(ptr @panic_msg, i64 1, i64 17, ptr %3)
  %5 = call i64 @strlen(ptr %2)
  %6 = call i64 @fwrite(ptr %2, i64 1, i64 %5, ptr %3)
  %7 = call i32 @fputc(i32 10, ptr %3)
  call void @abort()
  unreachable
}

declare ptr @strerror(i32)

declare i64 @fwrite(ptr, i64, i64, ptr)

declare i64 @strlen(ptr)

declare i32 @fputc(i32, ptr)

declare void @abort()

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
