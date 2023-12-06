#include <errno.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

extern intptr_t void_main(void *data, uintptr_t size);

int* get_errno();
const char* error_toCString(int error);
void panic(int error);

FILE* get_stdin();
FILE* get_stdout();
FILE* get_stderr();
