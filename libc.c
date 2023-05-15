#include <stdio.h>
#include <string.h>
#include <errno.h>

const char* error_toString(int error) {
	switch (error) {
		case 0: return "Not an error";
		case 256: return "Out of bounds array access";
		case 257: return "Optional value is None";
		case -1: return "Unexpected end of file";
		default: return strerror(error);
	}
}

void error_panic(int error) {
	const char *prefix = "(internal error) ";
	const char *msg = error_toString(error);
	fwrite(prefix, 1, strlen(prefix), stderr);
	fwrite(msg, 1, strlen(msg), stderr);
	fputc('\n', stderr);
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
