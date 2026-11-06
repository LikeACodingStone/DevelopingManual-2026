# JsonCpp: JSON Parsing and Writing for C++

- Aliases and ecosystem: JsonCpp / `Json::Value` (C++; not the C library cJSON and not Qt's `QJsonDocument`)
- Versions and platforms: based on the 1.9.x `CharReaderBuilder` / `StreamWriterBuilder` interface; needs the jsoncpp development package
- Tags: network
- Example status: not compiled: this machine lacks the jsoncpp development package; the check script compiles and runs it automatically once installed
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

JsonCpp parses JSON text into a `Json::Value` tree (null, integer, unsigned integer, real, string, boolean, array, object) and writes it back to text. Object members are stored sorted by key. The JSON text format is defined in RFC 8259.

Similar libraries have different interfaces and must not be mixed: [cJSON](../../network/json-cjson.md) (C) and [Qt JSON](../../network/qt-json.md) (Qt), both Chinese only.

## When to use

When a C++ project needs to read a whole JSON document into an in-memory tree and then access it. For very large documents, or when you only want to scan sequentially, consider a streaming (SAX-style) parser; when large integers or high-precision decimals must be preserved, handle their string form yourself.

## How to use

1. Install the jsoncpp development package and get compile flags from `pkg-config jsoncpp` or CMake's package configuration; the CMake target name varies with version and installation (for example `JsonCpp::JsonCpp`, `jsoncpp_lib`), so follow the installed package's configuration.
2. Parse: use `CharReaderBuilder`; for untrusted input call `CharReaderBuilder::strictMode()`, then `newCharReader()->parse(begin, end, &root, &errors)` and check the return value. The old `Json::Reader` is deprecated.
3. Check the type before reading (`isObject()`, `isString()`, `isInt()`); `asString()` and `asInt()` throw `Json::LogicError` on a mismatch or out-of-range value.
4. For read-only access use a `const` reference, `get(key, default)` or `isMember()`: `operator[]` on a non-const object inserts a null member and quietly changes the document.
5. Write: `StreamWriterBuilder`, set `indentation` to an empty string for compact output, and call `Json::writeString()`.
6. Limit the input size; the parser has a nesting-depth limit (`stackLimit`) that you should not loosen.

## Minimal example

Run the commands from the handbook root.

[jsoncpp_demo.cpp](../../../examples/native/jsoncpp_demo.cpp) shows strict parsing, typed access after a type check, defaults for missing keys, write-then-reparse comparison, and inputs that strict mode rejects (truncated, duplicate key, trailing content, trailing comma, unclosed array).

```sh
c++ -std=c++17 -Wall -Wextra -Werror examples/native/jsoncpp_demo.cpp $(pkg-config --cflags --libs jsoncpp) -o /tmp/jsoncpp-demo
/tmp/jsoncpp-demo
```

Expected: `JsonCpp strict parse and typed access OK`. The dependency is missing here and the example was not compiled, so it must not be treated as verified.

## FAQ

- The default lenient mode allows comments and lets a later duplicate key overwrite an earlier one; strict mode rejects duplicate keys, trailing content and so on, and is meant for untrusted input. Some options may not exist in older versions; follow the version actually installed.
- Integer range: test with `isInt()` or `isInt64()` instead of calling `asInt()` and checking afterwards.
- Projects that disable exceptions (`-fno-exceptions`) must handle the failure paths of `asX()` specially.
- Output keys are sorted by key, not in input order; do not rely on byte-for-byte text equality, reparse and compare instead.
- A declared submodule version is not the version actually linked; recheck the interface before upgrading.

## References

- [JsonCpp repository and documentation](https://github.com/open-source-parsers/jsoncpp)
- [RFC 8259: JSON](https://www.rfc-editor.org/rfc/rfc8259)
- [Example verification scope](../../../examples/README_EN.md)
