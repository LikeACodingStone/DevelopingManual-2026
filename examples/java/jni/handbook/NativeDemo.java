package handbook;

/**
 * JNI example (Java side). Status: NOT compiled here (no JDK). See topics for build commands.
 * Native methods are bound by name: Java_handbook_NativeDemo_<method>.
 */
public final class NativeDemo {
    static {
        System.loadLibrary("handbook_jni"); // libhandbook_jni.so on Linux; resolved via java.library.path
    }

    private NativeDemo() {
    }

    public static native String join(String a, String b);

    public static native int sum(int[] values);

    /** The handle is an opaque native pointer stored in a long. Never reuse it after destroy. */
    public static native long counterCreate();

    public static native int counterIncrement(long handle);

    public static native void counterDestroy(long handle);

    public static void main(String[] args) {
        if (!"a-b".equals(join("a", "b"))) {
            throw new AssertionError("join");
        }
        if (sum(new int[] {1, 2, 3}) != 6) {
            throw new AssertionError("sum");
        }
        try {
            sum(null);
            throw new AssertionError("null array must be rejected");
        } catch (IllegalArgumentException expected) {
            // native code raised it with ThrowNew
        }
        try {
            sum(new int[] {Integer.MAX_VALUE, 1});
            throw new AssertionError("overflow must be reported");
        } catch (ArithmeticException expected) {
            // native code detected the overflow
        }
        long handle = counterCreate();
        try {
            counterIncrement(handle);
            if (counterIncrement(handle) != 2) {
                throw new AssertionError("counter");
            }
        } finally {
            counterDestroy(handle);
        }
        System.out.println("JNI strings, arrays, exceptions and handles OK");
    }
}
