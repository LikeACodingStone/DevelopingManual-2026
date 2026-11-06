// Protobuf C++ runtime: serialize to / parse from a byte array, field presence, required
// fields and truncated input, using the proto2 schema legacy_v2.proto.
//
// Status: written against the protobuf C++ API; NOT compiled here (no protoc / protobuf development package).
// Build:  mkdir -p /tmp/handbook-proto-cpp
//         protoc -I examples/protobuf --cpp_out=/tmp/handbook-proto-cpp examples/protobuf/legacy_v2.proto
//         c++ -std=c++17 -Wall -Wextra -I/tmp/handbook-proto-cpp examples/protobuf/cpp_roundtrip.cpp \
//             /tmp/handbook-proto-cpp/legacy_v2.pb.cc $(pkg-config --cflags --libs protobuf) -o /tmp/proto-cpp
//         (use the protoc that matches the runtime library; newer runtimes may need a C++17 or later standard)
// Run:    /tmp/proto-cpp
#include "legacy_v2.pb.h"

#include <cstdint>
#include <iostream>
#include <vector>

namespace {

int fail(const char *what)
{
    std::cerr << "FAIL: " << what << '\n';
    return 1;
}

std::vector<std::uint8_t> encode(const handbook::v2::Reading &message)
{
    std::vector<std::uint8_t> wire(message.ByteSizeLong());
    // SerializeToArray fails when required fields are missing; check the result.
    if (!message.SerializeToArray(wire.data(), static_cast<int>(wire.size())))
        wire.clear();
    return wire;
}

} // namespace

int main()
{
    GOOGLE_PROTOBUF_VERIFY_VERSION;

    handbook::v2::Reading full;
    full.set_sensor_id(7);
    full.set_value(2.5);
    const std::vector<std::uint8_t> wire = encode(full);
    if (wire.empty())
        return fail("encode");

    handbook::v2::Reading parsed;
    if (!parsed.ParseFromArray(wire.data(), static_cast<int>(wire.size())))
        return fail("parse");
    if (parsed.sensor_id() != 7 || !parsed.has_value() || parsed.value() != 2.5)
        return fail("round trip values");

    // Presence: an unset optional reads as its declared default but has_*() stays false.
    handbook::v2::Reading minimal;
    minimal.set_sensor_id(1);
    const std::vector<std::uint8_t> minimal_wire = encode(minimal);
    handbook::v2::Reading minimal_parsed;
    if (minimal_wire.empty() || !minimal_parsed.ParseFromArray(minimal_wire.data(), static_cast<int>(minimal_wire.size())))
        return fail("minimal message");
    if (minimal_parsed.has_value() || minimal_parsed.value() != -1.0 || minimal_parsed.has_unit())
        return fail("presence and defaults");

    // A required field that is missing makes the message "uninitialized": serialize with the
    // *Partial* variant only to build bad input, and expect the strict parse to refuse it.
    handbook::v2::Reading incomplete;
    incomplete.set_value(1.0);
    if (incomplete.IsInitialized())
        return fail("required field not detected");
    std::vector<std::uint8_t> partial(incomplete.ByteSizeLong());
    incomplete.SerializePartialToArray(partial.data(), static_cast<int>(partial.size()));
    handbook::v2::Reading rejected;
    if (rejected.ParseFromArray(partial.data(), static_cast<int>(partial.size())))
        return fail("message without required field was accepted");

    // Truncated input must fail, not return a half-filled message.
    std::vector<std::uint8_t> truncated(wire.begin(), wire.end() - 1);
    handbook::v2::Reading from_truncated;
    if (from_truncated.ParseFromArray(truncated.data(), static_cast<int>(truncated.size())))
        return fail("truncated input was accepted");

    google::protobuf::ShutdownProtobufLibrary();
    std::cout << "Protobuf C++ round trip, presence and required fields OK\n";
    return 0;
}
