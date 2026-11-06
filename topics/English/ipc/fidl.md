# FIDL: First Decide Which Interface Definition Language

- Tags: interface description, code generation, inter-process communication
- Example status: syntax sketch only; the related SDKs are not installed and nothing was compiled

Two different technologies share the name FIDL. Their compilers, generated code and communication flows must not be mixed.

| Name | Purpose | Tools and runtime |
| --- | --- | --- |
| Fuchsia Interface Definition Language | Defines Fuchsia protocols, data types and methods | Fuchsia SDK / source build, fidlc, language bindings |
| Franca IDL | Defines interfaces, types and methods, commonly used with CommonAPI | Franca tools; CommonAPI scenarios need the core and a binding generator such as D-Bus or SOME/IP |

## Fuchsia FIDL

Used to define protocols between components and to generate language bindings. Platform tools handle encoding, decoding and message transport, while business code implements the protocol.

Syntax sketch:

```fidl
library handbook.echo;

closed protocol Echo {
    strict Echo(struct { value string:128; })
        -> (struct { value string:128; });
};
```

Steps:

1. Prepare a Fuchsia development environment that matches the target platform version.
2. Define the `.fidl` file and declare the FIDL library and binding dependencies in the build target.
3. Build to generate the client and server interfaces for the chosen language.
4. The server implements the methods and publishes the protocol capability; the client connects and calls.
5. Declare and route capabilities in the component manifest, and verify the calls in the target environment.

Writing a `.fidl` file alone does not make communication run. The actual build, binding API and component configuration must follow the documentation of the SDK in use.

## Franca IDL

Describes interfaces that are independent of the implementation language. With CommonAPI you also choose a communication binding; the IDL itself does not decide the transport.

Syntax sketch:

```fidl
package handbook

import handbook.Types.* from "Types.fidl"

<**
  @description : Echo service. Doc comments use <** ... **>.
**>
interface Echo {
    version { major 1 minor 0 }

    attribute UInt32 callCount readonly

    method echo {
        in { String text }
        out { String reply }
    }

    broadcast echoed {
        out { String text }
    }
}
```

Common elements:

- `package` and `import ... from "file"`: split types into other `.fidl` files and reference them.
- `version { major minor }`: the interface version. By convention a major change means incompatible and a minor change should stay compatible; Franca itself does not check compatibility.
- `method` (request/response), `broadcast` (the server pushes an event to subscribers) and `attribute` (state that can be read and written, optionally marked `readonly`).
- `<** ... **>`: a doc comment that a generator can carry into the generated code.

Steps:

1. Install a compatible CommonAPI core, the generator for the chosen binding, and the runtime libraries.
2. Write the `.fidl`; add `.fdepl` deployment information as the binding requires.
3. Run the generator to produce types, client proxies and server stubs.
4. Implement and register the server; the client creates a proxy and calls.
5. Configure a runtime such as D-Bus or SOME/IP and verify discovery and request/response.

The generator is not necessarily CommonAPI. Some projects use an in-house generator that reads `.fidl` and produces its own adaptation code (possibly targeting D-Bus, JSON messages or JNI). Then the deployment information, runtime libraries and transport are defined by that generator, and CommonAPI documentation does not apply.

## FAQ

- Ask which ecosystem it is before looking up FIDL usage.
- Generator, runtime library and binding versions must be compatible.
- Interface changes must consider compatibility on both sides; being able to regenerate code does not mean old clients still work.
- Neither FIDL is Android's [AIDL](../programming/android-aidl.md) or Protobuf: syntax, toolchain and transport all differ.
- Find out whether a project uses CommonAPI or an in-house generator before looking for the matching deployment files and runtime documentation.
- The snippets above only show the shape of an interface; they are not verified complete projects.

## References

- [Fuchsia FIDL](https://fuchsia.dev/fuchsia-src/development/languages/fidl)
- [Franca](https://github.com/franca/franca)
- [CommonAPI C++ documentation](https://covesa.github.io/capicxx-core-tools/)
