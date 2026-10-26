# SQLite 与 Qt SQL

- 别名与生态：SQLite / Python sqlite3 / Qt QSQLITE
- 适用版本与平台：Python 3 标准库；Qt 5/6 SQL 插件另需安装
- 标签：network
- 示例状态：Python 内存数据库已运行；Qt 示例未编译
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

SQLite 是嵌入进程的数据库引擎。Qt SQL 的 QSQLITE 驱动提供另一套访问接口，不是独立数据库服务器。

## 何时使用

本地配置、结构化结果、事务性记录。多进程写竞争与连接线程归属需要设计；远程多写者场景应评估其他数据库。

## 如何使用

1. 创建连接与表，明确主键和约束。
2. 使用参数绑定，避免拼接用户输入。
3. 将相关写入放入事务，失败时回滚。
4. 关闭查询和连接；Qt 的连接名须唯一，移除前销毁所有引用。

## 最小示例

以下命令从手册根目录执行。

[Python 示例](../../examples/python/sqlite_demo.py)验证参数绑定和重复主键引发的整笔事务回滚。

```sh
python3 examples/python/sqlite_demo.py
```

预期 `SQLite parameter binding and rollback OK`。

[Qt SQL 示例](../../examples/qt/sqlite_demo.cpp)使用独立内存库：

```sh
cmake -S examples/qt -B /tmp/handbook-qt
cmake --build /tmp/handbook-qt
```
```sh
/tmp/handbook-qt/sqlite_demo
```
预期 `Qt SQLite memory database OK`；Qt 示例未编译，运行还需要 QSQLITE 插件。

## 常见问题

`:memory:` 通常按连接隔离。普通 SQLite 不因设置用户名密码而获得文件加密。Qt 连接不要跨线程直接共享；忙等待、事务失败和磁盘满都应作为可恢复错误处理。

## 参考资料

- [SQLite 事务](https://www.sqlite.org/lang_transaction.html)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [QSqlDatabase](https://doc.qt.io/qt-6/qsqldatabase.html)
- [示例验证范围](../../examples/README.md)
