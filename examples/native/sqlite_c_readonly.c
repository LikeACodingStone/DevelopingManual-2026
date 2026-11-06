/*
 * SQLite C API: create a temporary database, then reopen it read-only and query with a
 * bound parameter. Shows the error paths: write on a read-only connection, missing file,
 * missing row.
 *
 * Status: written against the SQLite 3 C API; NOT compiled here (no sqlite3.h development package).
 * Build:  cc -std=c11 -Wall -Wextra -Werror examples/native/sqlite_c_readonly.c \
 *            $(pkg-config --cflags --libs sqlite3) -o /tmp/sqlite-c
 * Run:    /tmp/sqlite-c
 */
#define _XOPEN_SOURCE 700
#define _DEFAULT_SOURCE

#include <sqlite3.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static int fail(const char *what, sqlite3 *db)
{
    fprintf(stderr, "FAIL: %s%s%s\n", what, db ? ": " : "", db ? sqlite3_errmsg(db) : "");
    return 1;
}

static int build_database(const char *path)
{
    sqlite3 *db = NULL;
    if (sqlite3_open_v2(path, &db, SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE, NULL) != SQLITE_OK)
        return fail("create", db);
    int rc = sqlite3_exec(db, "CREATE TABLE area(code INTEGER PRIMARY KEY, name TEXT NOT NULL)", NULL, NULL, NULL);
    sqlite3_stmt *insert = NULL;
    if (rc == SQLITE_OK)
        rc = sqlite3_prepare_v2(db, "INSERT INTO area(code, name) VALUES(?1, ?2)", -1, &insert, NULL);
    if (rc == SQLITE_OK) {
        sqlite3_bind_int(insert, 1, 13);
        sqlite3_bind_text(insert, 2, "Tokyo", -1, SQLITE_STATIC);
        rc = sqlite3_step(insert) == SQLITE_DONE ? SQLITE_OK : SQLITE_ERROR;
    }
    sqlite3_finalize(insert); /* safe on NULL */
    if (rc != SQLITE_OK) {
        int code = fail("populate", db);
        sqlite3_close(db);
        return code;
    }
    sqlite3_close(db);
    return 0;
}

int main(void)
{
    char path[] = "/tmp/handbook-sqlite-XXXXXX";
    int fd = mkstemp(path);
    if (fd < 0)
        return 1;
    close(fd);

    int status = build_database(path);
    sqlite3 *db = NULL;

    if (status == 0) {
        if (sqlite3_open_v2(path, &db, SQLITE_OPEN_READONLY, NULL) != SQLITE_OK) {
            status = fail("open read-only", db);
        }
    }

    if (status == 0) {
        sqlite3_stmt *query = NULL;
        if (sqlite3_prepare_v2(db, "SELECT name FROM area WHERE code = ?1", -1, &query, NULL) != SQLITE_OK) {
            status = fail("prepare", db);
        } else {
            sqlite3_bind_int(query, 1, 13);
            if (sqlite3_step(query) != SQLITE_ROW ||
                strcmp((const char *)sqlite3_column_text(query, 0), "Tokyo") != 0)
                status = fail("expected row for code 13", db);
            sqlite3_reset(query); /* reuse with another parameter value */
            sqlite3_bind_int(query, 1, 99);
            if (status == 0 && sqlite3_step(query) != SQLITE_DONE)
                status = fail("code 99 must have no row", db);
            sqlite3_finalize(query);
        }
    }

    if (status == 0) { /* a read-only connection must refuse writes */
        char *message = NULL;
        int rc = sqlite3_exec(db, "INSERT INTO area VALUES(14, 'Kanagawa')", NULL, NULL, &message);
        sqlite3_free(message);
        if (rc != SQLITE_READONLY)
            status = fail("write on read-only connection was not refused", db);
    }
    sqlite3_close(db); /* NULL is allowed */

    if (status == 0) { /* a missing file is an error, and the handle must still be closed */
        sqlite3 *missing = NULL;
        int rc = sqlite3_open_v2("/nonexistent-dir/none.db", &missing, SQLITE_OPEN_READONLY, NULL);
        sqlite3_close(missing);
        if (rc == SQLITE_OK)
            status = fail("missing file opened", NULL);
    }

    unlink(path);
    if (status == 0)
        puts("SQLite C API read-only OK");
    return status;
}
