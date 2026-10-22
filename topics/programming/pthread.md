# pthread 线程与互斥锁

- 别名与生态：pthread 线程与互斥锁
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：programming
- 示例状态：复用组件 + 新并发驱动，已编译运行验证
- 代码来源：summary_components 线程组件复用，驱动新写

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

[计数器实现](../../examples/native/core_thread_example.c)直接复用原 summary_components 已迁移的线程组件；[新驱动](../../examples/native/threads.c)用两个线程验证。

```sh
cc -std=c11 -Wall -Wextra -pthread examples/native/core_thread_example.c examples/native/threads.c -o /tmp/threads-demo
/tmp/threads-demo
```

预期 `counter=20000`。

## 常见问题

复用实现假定 mutex 初始化成功且生命周期正确，不处理误用导致的 lock/unlock 错误。int 计数器还应避免溢出。不能销毁正在使用的锁，不能用 volatile 替代同步。

## 参考资料

- [官方资料或明确标注的技术参考](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/pthread.h.html)
- [代码来源与验证范围](../../sources.md)
