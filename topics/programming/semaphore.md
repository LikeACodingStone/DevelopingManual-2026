# POSIX 信号量

- 别名与生态：POSIX 信号量
- 适用版本与平台：见使用步骤和示例依赖；不继承历史工程版本
- 标签：programming
- 示例状态：新 C 示例已编译运行
- 代码来源：为本手册新写；不引用 2016Codes 代码

## 是什么

信号量维护一个非负计数。post 增加计数，wait 消耗一个许可；计数为零时等待。互斥锁用于保护临界区，信号量常用于事件或资源数量同步。

## 何时使用

生产者通知消费者、限制并发资源。本例演示一个生产者完成写入后通知主线程读取。

## 如何使用

1. sem_init(pshared=0, value=0) 创建线程间信号量。
2. 生产者写好数据后 sem_post。
3. 消费者 sem_wait，遇 EINTR 重试。
4. join 线程后销毁信号量。

## 最小示例

以下命令均从仓库根目录运行。

[新信号量示例](../../examples/native/semaphore.c)：

```sh
cc -std=c11 -Wall -Wextra -pthread examples/native/semaphore.c -o /tmp/sem-demo
/tmp/sem-demo
```

预期 `value=42`。

## 常见问题

一个 post 只提供一个许可，不是广播。重复使用共享槽位还需防止生产者覆盖未读取的数据，通常需要空槽/满槽两个信号量。销毁前确保没有等待者。

## 参考资料

- [官方资料或明确标注的技术参考](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/semaphore.h.html)
- [代码来源与验证范围](../../sources.md)
