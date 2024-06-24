[![main](https://github.com/ge0mk/void/actions/workflows/main.yml/badge.svg)](https://github.com/ge0mk/void/actions/workflows/main.yml)

void - language & compiler
==

dependencies
--
- llvm >= 17.0 (binaries, headers & clang)

build the compiler
--
```bash
git clone https://github.com/ge0mk/void
cd void
make
```

hello world
--
```
import std/core;
import std/string;
import std/io;
func main() -> void {
	println("Hello world!");
}
```
