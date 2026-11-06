# SQLite（C API、Python 与 Qt SQL）

- 别名与生态：SQLite / SQLite C API（`sqlite3_*`）/ Python sqlite3 / Qt QSQLITE
- 适用版本与平台：Python 3 标准库；C API 需要 sqlite3 开发包；Qt 5/6 SQL 插件另需安装
- 标签：network
- 示例状态：Python 内存数据库已运行；C API 与 Qt 示例未编译
- 代码来源：本手册独立新写，所有教学代码位于 examples/；不引用历史工程源码

## 是什么

SQLite 是嵌入进程的数据库引擎。C API（`sqlite3_open_v2`、`sqlite3_prepare_v2`、`sqlite3_step` 等）是最底层的接口，Python 的 `sqlite3` 模块和 Qt SQL 的 QSQLITE 驱动都是它的封装，各有自己的接口，不是独立数据库服务器。

## 何时使用

本地配置、结构化结果、事务性记录，以及随程序发布的只读查询表。多进程写竞争与连接线程归属需要设计；远程多写者场景应评估其他数据库。

## 如何使用

1. 创建连接与表，明确主键和约束。
2. 使用参数绑定，避免拼接用户输入。
3. 将相关写入放入事务，失败时回滚。
4. 关闭查询和连接；Qt 的连接名须唯一，移除前销毁所有引用。

C API 的流程：

1. `sqlite3_open_v2(路径, &db, 标志, NULL)`。只查询随程序发布的数据库时用 `SQLITE_OPEN_READONLY`，这样误写会得到 `SQLITE_READONLY` 而不是改坏文件。
2. 打开失败时 `db` 仍可能非空，也要调用 `sqlite3_close(db)` 释放，错误信息用 `sqlite3_errmsg(db)` 读取。
3. `sqlite3_prepare_v2` 编译语句，`sqlite3_bind_*` 绑定参数（序号从 1 开始），循环 `sqlite3_step`：返回 `SQLITE_ROW` 表示有一行，`SQLITE_DONE` 表示结束，其他值是错误。
4. 用 `sqlite3_column_*` 读取列；`sqlite3_column_text` 返回的指针只在下一次 `step`、`reset` 或 `finalize` 之前有效，需要保留就先复制。
5. 重复执行同一语句用 `sqlite3_reset` 后重新绑定；用完必须 `sqlite3_finalize`，否则关闭连接时会残留未完成的语句。

## 最小示例

以下命令从手册根目录执行。

[Python 示例](../../examples/python/sqlite_demo.py)验证参数绑定和重复主键引发的整笔事务回滚。

```sh
python3 examples/python/sqlite_demo.py
```

预期 `SQLite parameter binding and rollback OK`。

[C API 示例](../../examples/native/sqlite_c_readonly.c)先创建临时数据库，再以只读方式重新打开，用绑定参数查询，并检查三条失败路径：只读连接写入被拒绝、查询不存在的行得到 `SQLITE_DONE`、打开不存在的文件失败但仍释放句柄。

```sh
cc -std=c11 -Wall -Wextra -Werror examples/native/sqlite_c_readonly.c $(pkg-config --cflags --libs sqlite3) -o /tmp/sqlite-c
/tmp/sqlite-c
```

预期 `SQLite C API read-only OK`；本机缺 `sqlite3.h` 开发包，C 示例未编译，不能当作已通过验证。

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

`:memory:` 通常按连接隔离。普通 SQLite 不因设置用户名密码而获得文件加密。Qt 连接不要跨线程直接共享；忙等待（`SQLITE_BUSY`）、事务失败和磁盘满都应作为可恢复错误处理。

C API 特别要注意：不要用字符串拼接构造 SQL；每个 `prepare` 都要有 `finalize`；`sqlite3_open_v2` 的只读标志不等于文件系统权限；`sqlite3_prepare`（旧版）与 `sqlite3_prepare_v2` 的错误报告方式不同，新代码用 `_v2`。随程序发布的数据库文件要和读取它的程序版本一起管理，不要假设表结构不变。

## 参考资料

- [SQLite 事务](https://www.sqlite.org/lang_transaction.html)
- [SQLite C/C++ 接口](https://www.sqlite.org/cintro.html)
- [sqlite3_open_v2 标志](https://www.sqlite.org/c3ref/open.html)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [QSqlDatabase](https://doc.qt.io/qt-6/qsqldatabase.html)
- [示例验证范围](../../examples/README.md)
