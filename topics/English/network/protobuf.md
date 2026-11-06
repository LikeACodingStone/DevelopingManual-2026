# Protocol Buffers: Structured Binary Messages

- Aliases and ecosystem: Protobuf / proto2 / proto3; Python and C++ runtime libraries
- Versions and platforms: proto2 and proto3; protoc and the runtime library (Python protobuf, C++ libprotobuf) must be compatible versions
- Tags: network
- Example status: not run: protoc, Python protobuf and the C++ development package are missing
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

Protocol Buffers define messages with a schema and field numbers and generate serialization APIs. They provide no TCP message boundaries, no encryption and no checking of business-field validity.

The schema has two syntaxes, and both can exist in the same project:

| Aspect | proto2 | proto3 |
| --- | --- | --- |
| Declaration | `syntax = "proto2";` | `syntax = "proto3";` |
| Required fields | `required` exists (not recommended for new fields, because it can never be safely removed later) | none |
| Field presence | every `optional` field has `has_*()` | plain scalar fields have no presence; use `optional` or `oneof` to get it |
| Defaults | customizable with `[default = ...]` | fixed to the zero value; not customizable |

## When to use

Cross-process messages, structured result storage and version evolution. Both ends need the shared schema; it is less readable than JSON when debugging.

## How to use

1. Define field numbers and types; after deleting a field keep its number and never reassign it.
2. Generate the target-language bindings with a matching protoc.
3. Validate business fields before encoding and limit the message length before decoding.
4. Preserve message boundaries in the transport layer; even after a successful parse, check ranges and required business constraints.

Key points for the C++ runtime:

- Serialize to an array: get the size with `ByteSizeLong()` first, then `SerializeToArray(buffer, size)`, and check the return value; serialization fails when a proto2 `required` field is missing.
- Parse: `ParseFromArray(data, length)`; a `false` return means truncated data, malformed data or a missing required field, and the target object must not be used then.
- Presence: proto2 uses `has_xxx()` to tell "not set" from "set to the default"; reading a field that is not set gives the declared default.
- `SerializePartialToArray` can serialize an uninitialized message; use it only to build test input or for debugging.
- Check at program start with `GOOGLE_PROTOBUF_VERIFY_VERSION` that the header and the library versions agree, and call `ShutdownProtobufLibrary()` at the end if you want.

## Minimal example

Run the commands from the handbook root.

The [new schema](../../../examples/protobuf/sample.proto) and the [round-trip check](../../../examples/protobuf/roundtrip.py) use only synthetic measurements.

```sh
mkdir -p /tmp/handbook-proto
protoc -I examples/protobuf --python_out=/tmp/handbook-proto examples/protobuf/sample.proto
PYTHONPATH=/tmp/handbook-proto python3 examples/protobuf/roundtrip.py
```

Expected: `Protobuf roundtrip and malformed input OK`; dependencies are missing now, so it was not executed. The generated files are temporary build products; all teaching sources are in this repository.

The [proto2 schema](../../../examples/protobuf/legacy_v2.proto) and the [C++ round-trip check](../../../examples/protobuf/cpp_roundtrip.cpp) show a `required` field, `has_value()` and defaults, rejection of data that lacks a required field, and rejection of truncated input.

```sh
mkdir -p /tmp/handbook-proto-cpp
protoc -I examples/protobuf --cpp_out=/tmp/handbook-proto-cpp examples/protobuf/legacy_v2.proto
c++ -std=c++17 -Wall -Wextra -I/tmp/handbook-proto-cpp examples/protobuf/cpp_roundtrip.cpp /tmp/handbook-proto-cpp/legacy_v2.pb.cc $(pkg-config --cflags --libs protobuf) -o /tmp/proto-cpp
/tmp/proto-cpp
```

Expected: `Protobuf C++ round trip, presence and required fields OK`; protoc and the C++ development package are missing, so it was not compiled and must not be treated as verified.

## FAQ

A default value is not the same as the field being explicitly present; use optional or oneof of a suitable version when you need presence. Changing a field number breaks compatibility; limit nesting depth, size and untrusted input. Together with TCP framing ([Chinese only](../../network/tcp-framing.md)), do not treat one network read as one Protobuf message.

proto2 and proto3 messages can parse each other (field numbers and the wire format are the same), but the semantics of `required`, defaults and presence differ, so check field by field before mixing them. A mismatch between generated code and the runtime library often comes from upgrading one side but not the other; newer runtimes also have C++ standard requirements, so follow the documentation of the version used. A submodule or branch version declared by a project is not the version actually linked.

## References

- [proto3 guide](https://protobuf.dev/programming-guides/proto3/)
- [proto2 guide](https://protobuf.dev/programming-guides/proto2/)
- [C++ generated code guide](https://protobuf.dev/reference/cpp/cpp-generated/)
- [Generated code and runtime compatibility](https://protobuf.dev/support/cross-version-runtime-guarantee/)
- [Example verification scope](../../../examples/README_EN.md)
