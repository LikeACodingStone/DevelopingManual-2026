"""Independent in-memory SQL example; no project databases."""
import sqlite3

def main():
    db = sqlite3.connect(':memory:')
    try:
        db.execute('CREATE TABLE samples (id INTEGER PRIMARY KEY, value REAL NOT NULL)')
        with db:
            db.execute('INSERT INTO samples VALUES (?, ?)', (1, 2.5))
        try:
            with db:
                db.execute('INSERT INTO samples VALUES (?, ?)', (2, 3.5))
                db.execute('INSERT INTO samples VALUES (?, ?)', (1, 4.5))
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError('duplicate key accepted')
        assert db.execute('SELECT id, value FROM samples').fetchall() == [(1, 2.5)]
        print('SQLite parameter binding and rollback OK')
    finally:
        db.close()

if __name__ == '__main__':
    main()
