# JNI：Java 与本地代码互调

- 别名与生态：Java Native Interface / JNI（Android 上通过 NDK 使用同一规范）
- 适用版本与平台：JDK 8 及以上的 JNI 规范；示例面向 Linux，Android 的库打包不同
- 标签：programming
- 示例状态：未编译：本机缺 JDK 与 `jni.h`；检查脚本在设置 `JAVA_HOME` 后会自动编译运行
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

JNI 让 Java 方法调用 C/C++ 编写的共享库，也让本地代码调用 Java。Java 一侧声明 `native` 方法并用 `System.loadLibrary` 加载库；本地一侧实现以 `JNIEnv*` 开头的函数。`JNIEnv` 属于当前线程，不能跨线程保存。

## 何时使用

复用现有 C/C++ 库、访问平台能力。边界调用有开销，不适合频繁的细粒度调用；能用纯 Java 实现的不必引入本地代码，因为本地代码的错误会使整个 JVM 崩溃，而不是抛出异常。

## 如何使用

1. Java 声明 `native` 方法，静态初始化块里 `System.loadLibrary("name")`，在 Linux 上对应 `libname.so`。
2. 用 `javac -h <目录>` 生成 C 头文件，本地源码包含它，签名不一致会在编译时暴露。
3. 函数名遵循 `Java_<包>_<类>_<方法>` 约定（包名中的点变下划线，名字里的下划线写成 `_1`）；也可以在 `JNI_OnLoad` 里用 `RegisterNatives` 显式注册。
4. 编译成共享库，头文件路径为 `$JAVA_HOME/include` 与 `$JAVA_HOME/include/linux`；运行时用 `-Djava.library.path` 指向库目录。
5. 字符串：`GetStringUTFChars` 返回的是 modified UTF-8（`U+0000` 与增补字符的编码与标准 UTF-8 不同），每次 Get 都要有对应的 Release。
6. 数组：`Get<Type>ArrayElements` 配 `Release<Type>ArrayElements`；只读时用 `JNI_ABORT` 避免拷回。
7. 异常：本地代码不能用 C++ 异常通知 Java；用 `ThrowNew`，此后立即返回，不要继续调用多数 JNI 函数。调用 Java 方法之后用 `ExceptionCheck` 检查。
8. 引用：本地引用在 native 方法返回时释放，循环里大量创建要 `DeleteLocalRef`；要跨调用保存对象必须 `NewGlobalRef` 并在不用时 `DeleteGlobalRef`。
9. 线程：本地创建的线程在调用 Java 之前必须 `AttachCurrentThread`，结束前 `DetachCurrentThread`。
10. 把本地对象指针保存在 `long` 里时，要自行防止释放后继续使用和重复释放。

## 最小示例

以下命令从手册根目录执行，需要 JDK；`JAVA_HOME` 指向 JDK 目录。

[NativeDemo.java](../../../examples/java/jni/handbook/NativeDemo.java)与[handbook_jni.c](../../../examples/java/jni/handbook_jni.c)演示：字符串拼接（含空值检查）、`int[]` 求和（空数组引用与溢出分别抛出 `IllegalArgumentException`、`ArithmeticException`）、用 `long` 保存本地计数器句柄。

```sh
mkdir -p /tmp/handbook-jni/include /tmp/handbook-jni/classes
javac -h /tmp/handbook-jni/include -d /tmp/handbook-jni/classes examples/java/jni/handbook/NativeDemo.java
cc -std=c11 -Wall -Wextra -Werror -fPIC -shared -I/tmp/handbook-jni/include -I"$JAVA_HOME/include" -I"$JAVA_HOME/include/linux" examples/java/jni/handbook_jni.c -o /tmp/handbook-jni/libhandbook_jni.so
java -Djava.library.path=/tmp/handbook-jni -cp /tmp/handbook-jni/classes handbook.NativeDemo
```

预期 `JNI strings, arrays, exceptions and handles OK`。当前缺 JDK，未编译，不能当作已通过验证。

## 常见问题

- `UnsatisfiedLinkError`：库名、搜索路径、32/64 位、函数名或签名不匹配；用 `javac -h` 生成的头文件可提前发现签名问题。
- 本地线程里 `FindClass` 找不到应用类：它使用系统类加载器，需要在 Java 线程里先取得类并保存全局引用。
- JVM 直接崩溃：多半是使用了已释放的引用、数组越界或跨线程使用 `JNIEnv`。
- 在 Android 上，库按 ABI 分目录打包，需要为每个目标 ABI 编译；`System.loadLibrary` 同样去掉 `lib` 前缀和 `.so` 后缀。
- 数组和字符串的拷贝开销可能很大，批量传递时设计好接口，避免逐元素调用。

## 参考资料

- [JNI 规范（Java SE 21）](https://docs.oracle.com/en/java/javase/21/docs/specs/jni/index.html)
- [Android JNI 提示](https://developer.android.com/training/articles/perf-jni)
- [示例验证范围](../../../examples/README.md)
