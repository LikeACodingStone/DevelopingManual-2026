# Qt 线程与队列信号槽

- 别名与生态：QObject / QThread / QueuedConnection
- 适用版本与平台：Qt 5/6 Core；C++17
- 标签：programming
- 示例状态：未编译：缺 Qt 开发包
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

QObject 具有线程归属。队列连接把调用投递到接收对象所在线程的事件循环；QThread 对象本身通常仍属于创建它的线程。

## 何时使用

让后台任务与 UI 或事件驱动通信分离。共享内存仍需同步；信号槽不自动消除数据竞争。

## 如何使用

1. 创建无父对象的 worker，把它移入目标线程。
2. 通过队列连接调度任务，确保事件循环正在运行。
3. 在拥有对象的线程中操作其定时器和通信对象。
4. 采用协作停止，调用 quit 和 wait；在线程结束时安排 worker 删除。

## 最小示例

以下命令从手册根目录执行。

[新线程示例](../../examples/qt/threads_demo.cpp)检查工作线程身份，用原子状态回传结果并回收线程。

```sh
cmake -S examples/qt -B /tmp/handbook-qt
cmake --build /tmp/handbook-qt
```
```sh
/tmp/handbook-qt/threads_demo
```
预期 `Qt worker thread and shutdown OK`；当前未执行。

## 常见问题

有父对象的 QObject 不能直接 moveToThread。quit 不会中断正在执行的阻塞函数；生产任务必须有可取消 I/O 和超时。不要使用 terminate 作为正常退出流程。GUI 对象留在主线程。

## 参考资料

- [QThread](https://doc.qt.io/qt-6/qthread.html)
- [Threads and QObjects](https://doc.qt.io/qt-6/threads-qobject.html)
- [示例验证范围](../../examples/README.md)
