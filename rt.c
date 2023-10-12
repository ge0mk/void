#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

const char* error_toCString(int error) {
	switch (error) {
		case 0: return "Not an error";
		case 256: return "Out of bounds array access";
		case 257: return "Optional value is None";
		case -1: return "Unexpected end of file";
		default: return strerror(error);
	}
}

void error_panic(int error) {
	const char *prefix = "PANIC: ";
	const char *msg = error_toCString(error);
	fwrite(prefix, 1, strlen(prefix), stderr);
	fwrite(msg, 1, strlen(msg), stderr);
	fputc('\n', stderr);
	abort();
}

int* get_errno() {
	return &errno;
}

FILE* get_stdin() {
	return stdin;
}

FILE* get_stdout() {
	return stdout;
}

FILE* get_stderr() {
	return stderr;
}

extern int64_t void_main(void *data, uint64_t size);

int main(int argc, char *argv[]) {
	struct {
		char *data;
		uint64_t size;
		uint64_t capacity;
		uint64_t short_size_and_flags;
	} args[argc];

	for(int i = 0; i < argc; i++) {
		args[i].data = argv[i];
		args[i].size = strlen(argv[i]);
		args[i].capacity = 0;
		args[i].short_size_and_flags = 0;
	}

	return void_main(&args, argc);
}
