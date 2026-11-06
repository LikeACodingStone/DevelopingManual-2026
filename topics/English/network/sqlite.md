# SQLite (C API, Python and Qt SQL)

- Aliases and ecosystem: SQLite / the SQLite C API (`sqlite3_*`) / Python sqlite3 / Qt QSQLITE
- Versions and platforms: Python 3 standard library; the C API needs the sqlite3 development package; the Qt 5/6 SQL plugin is installed separately
- Tags: network
- Example status: the Python in-memory database example has been run; the C API and Qt examples were not compiled
- Code source: written independently for this handbook; all teaching code is in examples/; no historical project source is referenced

## What it is

SQLite is a database engine embedded in the process. The C API (`sqlite3_open_v2`, `sqlite3_prepare_v2`, `sqlite3_step` and so on) is the lowest-level interface; Python's `sqlite3` module and the Qt SQL QSQLITE driver are both wrappers around it, each with its own interface. It is not a stand-alone database server.

## When to use

Local configuration, structured results, transactional records, and read-only lookup tables shipped with a program. Write contention between processes and connection thread ownership need design; for remote multi-writer scenarios evaluate other databases.

## How to use

1. Create the connection and tables, with explicit primary keys and constraints.
2. Use parameter binding and avoid concatenating user input.
3. Put related writes in a transaction and roll back on failure.
4. Close queries and connections; Qt connection names must be unique, and all references must be destroyed before removal.

The C API flow:

1. `sqlite3_open_v2(path, &db, flags, NULL)`. For a database shipped with the program that you only query, use `SQLITE_OPEN_READONLY`, so an accidental write gets `SQLITE_READONLY` instead of damaging the file.
2. When opening fails, `db` may still be non-null and must be released with `sqlite3_close(db)`; read the message with `sqlite3_errmsg(db)`.
3. `sqlite3_prepare_v2` compiles the statement, `sqlite3_bind_*` binds parameters (numbered from 1), and you loop on `sqlite3_step`: `SQLITE_ROW` means a row is available, `SQLITE_DONE` means the end, and anything else is an error.
4. Read columns with `sqlite3_column_*`; the pointer returned by `sqlite3_column_text` is valid only until the next `step`, `reset` or `finalize`, so copy it if you need to keep it.
5. To run the same statement again, call `sqlite3_reset` and rebind; always `sqlite3_finalize` when done, otherwise unfinished statements remain when the connection is closed.

## Minimal example

Run the commands from the handbook root.

The [Python example](../../../examples/python/sqlite_demo.py) verifies parameter binding and whole-transaction rollback caused by a duplicate primary key.

```sh
python3 examples/python/sqlite_demo.py
```

Expected: `SQLite parameter binding and rollback OK`.

The [C API example](../../../examples/native/sqlite_c_readonly.c) first creates a temporary database, reopens it read-only, queries with a bound parameter, and checks three failure paths: a write on the read-only connection is refused, a query for a missing row gets `SQLITE_DONE`, and opening a missing file fails while the handle is still released.

```sh
cc -std=c11 -Wall -Wextra -Werror examples/native/sqlite_c_readonly.c $(pkg-config --cflags --libs sqlite3) -o /tmp/sqlite-c
/tmp/sqlite-c
```

Expected: `SQLite C API read-only OK`. The `sqlite3.h` development package is missing here, so the C example was not compiled and must not be treated as verified.

The [Qt SQL example](../../../examples/qt/sqlite_demo.cpp) uses an independent in-memory database:

```sh
cmake -S examples/qt -B /tmp/handbook-qt
cmake --build /tmp/handbook-qt
```
```sh
/tmp/handbook-qt/sqlite_demo
```
Expected: `Qt SQLite memory database OK`; the Qt example was not compiled, and running it also needs the QSQLITE plugin.

## FAQ

`:memory:` is normally isolated per connection. Ordinary SQLite does not gain file encryption by setting a user name and password. Do not share a Qt connection directly across threads; busy waits (`SQLITE_BUSY`), failed transactions and a full disk should all be handled as recoverable errors.

Specific cautions for the C API: never build SQL by string concatenation; every `prepare` needs a `finalize`; the read-only flag of `sqlite3_open_v2` is not the same as file-system permissions; the older `sqlite3_prepare` and `sqlite3_prepare_v2` report errors differently, so new code uses `_v2`. A database file shipped with a program must be managed together with the version of the program that reads it; do not assume the table layout never changes.

## References

- [SQLite transactions](https://www.sqlite.org/lang_transaction.html)
- [SQLite C/C++ interface](https://www.sqlite.org/cintro.html)
- [sqlite3_open_v2 flags](https://www.sqlite.org/c3ref/open.html)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [QSqlDatabase](https://doc.qt.io/qt-6/qsqldatabase.html)
- [Example verification scope](../../../examples/README_EN.md)
