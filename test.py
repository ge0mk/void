#!/usr/bin/python3

import time
import os
import re
import subprocess
import sys

def delete_file(path):
    try:
        os.remove(path)
    except:
        pass

def find_tests():
	for root, dirs, files in os.walk("tests"):
		for file in files:
			if file[-3:] == ".vd":
				yield os.path.join(root, file)

def parse_test(test):
	result = []
	with open(test) as file:
		for line in file:
			if line == "//> skip\n":
				return "skip"

			if line == "//> test-crash\n":
				result.append(("test-crash", ""))
				continue

			match = re.match(r"//>\s*(error|output|compiler-ec|test-ec|compiler-arg|test-arg)\s*\"(.*)\"\s*\Z", line)

			if line[0:3] == "//>" and match is None:
				print("  invalid test specification: " + line, end="")
				return None

			if match is None:
				break

			type, output = match.group(1, 2)
			result.append((type, output.encode('latin-1', 'backslashreplace').decode('unicode-escape')))

	return result

def check_output(output, line):
	for output_line in output:
		if line in output_line:
			return True

	return False

def run_test(test, expected_result, compiler_args, memcheck, compiler):
	compile_cmd = [compiler, test, "-o", "test"] + compiler_args

	for type, value in expected_result:
		if type == "compiler-arg":
			compile_cmd += [value]

	compile_result = subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	compile_output = compile_result.stdout.decode("utf-8").split("\n")
	compile_error_is_success = False
	for type, value in expected_result:
		match type:
			case "compiler-ec":
				if compiler_result.returncode != int(value):
					return False, compile_result
				compile_error_is_success = True
			case "error":
				if not check_output(compile_output, value):
					# expected output not found -> test failed
					return False, compile_result
				compile_error_is_success = True
			case _:
				pass
	if compile_result.returncode != 0 or not os.path.exists("build/test"):
		return compile_error_is_success, compile_result

	test_cmd = []
	if memcheck:
		test_cmd = ["valgrind", "--leak-check=full", "--track-origins=yes", "build/test"]
	else:
		test_cmd = ["build/test"]

	for type, value in expected_result:
		if type == "test-arg":
			test_cmd += [value]

	test_result = subprocess.run(test_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	delete_file("build/test")
	delete_file("build/test.ll")
	delete_file("build/test.bc")


	test_output = [line + "\n" for line in test_result.stdout.decode("utf-8").split("\n")]
	test_error_is_success = False
	for type, value in expected_result:
		match type:
			case "test-crash":
				if test_result.returncode >= 0:
					return False, test_result
				test_error_is_success = True
			case "test-ec":
				if test_result.returncode != int(value):
					return False, test_result
				test_error_is_success = True
			case "output":
				if not check_output(test_output, value):
					# expected output not found -> test failed
					return False, test_result
			case _:
				pass

	if memcheck:
		if not check_output(test_output, "All heap blocks were freed -- no leaks are possible"):
			return False, test_result
		if check_output(test_output, "Use of uninitialised value"):
			return False, test_result
		if check_output(test_output, "Conditional jump or move depends on uninitialised value(s)"):
			return False, test_result
		if check_output(test_output, "Invalid read"):
			return False, test_result
		if check_output(test_output, "Invalid write"):
			return False, test_result

	# expected output -> test passed
	if test_result.returncode != 0 and not test_error_is_success:
		return False, test_result
	return True, test_result

def format_test_stats(failed, skipped, successful, total, current):
	return f"\r\x1b[2K[\x1b[1;31m{failed}\x1b[m|\x1b[1;33m{skipped}\x1b[m|\x1b[1;32m{successful}\x1b[m|{total}] {current}"

def main():
	start_time = time.time()
	args = []
	compiler_args = []
	compiler_path = sys.argv[1]

	try:
		args = sys.argv[2:sys.argv.index("--")]
		compiler_args = sys.argv[sys.argv.index("--") + 1:]
	except IndexError:
		args = sys.argv[2:]

	tests = [test for test in find_tests()]
	total = len(tests)
	failed = 0
	successful = 0
	skipped = 0

	for test in tests:
		expected_result = parse_test(test)
		if expected_result is None:
			failed += 1
			print("\r\x1b[2K[\x1b[31;1mFAIL\x1b[m] ", test)
			continue

		if expected_result == "skip":
			skipped += 1
			print(format_test_stats(failed, skipped, successful, total, "skipping " + test))
			continue

		print(format_test_stats(failed, skipped, successful, total, test), end="", flush=True)
		result, output = run_test(test, expected_result, compiler_args=compiler_args, memcheck=("--memcheck" in args), compiler=compiler_path)
		print("", end="\r")
		if result:
			successful += 1
		else:
			failed += 1
			print("\r\x1b[2K[\x1b[31;1mFAIL\x1b[m] ", test)
			output_text = output.stdout.decode("utf-8")
			if not "-q" in args:
				if output_text != "":
					print(output_text)
				print(f"-> {output.returncode}")

	status = ("completed successfully" if failed == 0 else "failed")
	print(format_test_stats(failed, skipped, successful, total, f"{status} in {time.time() - start_time:.3f} sec"))
	if failed > 0:
		exit(1)
	else:
		exit(0)

if __name__ == "__main__":
	main()
