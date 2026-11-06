// JsonCpp: strict parsing, typed access, and writing. Local data only.
//
// Status: written against the JsonCpp 1.9.x API; NOT compiled here (no jsoncpp development package).
// Build:  c++ -std=c++17 -Wall -Wextra -Werror examples/native/jsoncpp_demo.cpp \
//            $(pkg-config --cflags --libs jsoncpp) -o /tmp/jsoncpp-demo
// Run:    /tmp/jsoncpp-demo
#include <json/json.h>

#include <iostream>
#include <memory>
#include <string>

namespace {

bool parse_strict(const std::string &text, Json::Value &out, std::string &errors)
{
    Json::CharReaderBuilder builder;
    Json::CharReaderBuilder::strictMode(&builder.settings_); // no comments, no duplicate keys, no trailing text
    std::unique_ptr<Json::CharReader> reader(builder.newCharReader());
    return reader->parse(text.data(), text.data() + text.size(), &out, &errors);
}

int fail(const char *what)
{
    std::cerr << "FAIL: " << what << '\n';
    return 1;
}

} // namespace

int main()
{
    Json::Value request;
    std::string errors;
    if (!parse_strict(R"({"kind":"request","name":"read","params":{"key":"k1","retries":3}})", request, errors))
        return fail("valid document rejected");

    // Check types before converting: asString()/asInt() throw Json::LogicError on a mismatch.
    if (!request.isObject() || !request["name"].isString() || !request["params"].isObject())
        return fail("unexpected shape");
    const std::string name = request["name"].asString();
    const Json::Value &params = request["params"];
    // get() returns the default for a missing member; operator[] on a NON-const value would
    // insert a null member, which silently changes the document you are inspecting.
    const int retries = params.get("retries", 1).isInt() ? params["retries"].asInt() : 1;
    const int timeout = params.get("timeout", 30).asInt(); // absent -> default 30
    if (name != "read" || retries != 3 || timeout != 30 || request["params"].isMember("timeout"))
        return fail("typed access");

    // Writing: compact output, then parse it back instead of comparing text byte for byte.
    Json::Value reply(Json::objectValue);
    reply["kind"] = "response";
    reply["ok"] = true;
    reply["value"] = 3.5;
    Json::StreamWriterBuilder writer;
    writer["indentation"] = "";
    const std::string text = Json::writeString(writer, reply);
    Json::Value reparsed;
    if (!parse_strict(text, reparsed, errors) || reparsed != reply)
        return fail("write/parse round trip");

    // Inputs that strict mode must reject.
    const char *bad[] = {R"({"a":)", R"({"a":1,"a":2})", R"({} trailing)", R"({"a":1,})", "[1,2"};
    for (const char *document : bad) {
        Json::Value ignored;
        if (parse_strict(document, ignored, errors))
            return fail(document);
    }

    std::cout << "JsonCpp strict parse and typed access OK\n";
    return 0;
}
