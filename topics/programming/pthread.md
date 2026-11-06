# pthread 线程与互斥锁

- 别名与生态：pthread 线程与互斥锁
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：programming
- 示例状态：独立新写双线程计数器，已编译运行验证
- 代码来源：本手册独立新写，源码仅位于 examples/native/threads.c

## 是什么

POSIX 线程共享进程地址空间。互斥锁让同一临界区不会被多个线程同时执行；共享变量的普通读写本身不提供同步保证。

## 何时使用

后台工作线程、共享状态与并发计数。线程结束前不能销毁它仍在使用的锁或上下文。

## 如何使用

1. 初始化共享对象与互斥锁。
2. 创建线程，确保参数在所有线程退出前仍有效。
3. 对共享变量的读写使用同一把锁。
4. join 所有线程后获取最终结果。
5. 销毁锁。

## 最小示例

以下命令均从仓库根目录运行。

[独立计数器示例](../../examples/native/threads.c)用两个线程递增共享计数器，并检查 pthread 返回码。

```sh
cc -std=c11 -Wall -Wextra -pthread examples/native/threads.c -o /tmp/threads-demo
/tmp/threads-demo
```

预期 `counter=20000`。

## 常见问题

示例限制递增次数以避免计数溢出；创建第二个线程失败时会回收已经创建的线程。同步原语失败时示例立即结束进程，不演示复杂恢复。不能销毁正在使用的锁，不能用 volatile 替代同步。

## 参考资料

- [官方资料或明确标注的技术参考](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/pthread.h.html)
- [代码来源与验证范围](../../catalog/Chinese/sources.md)
