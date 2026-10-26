#include <QCoreApplication>
#include <QSqlDatabase>
#include <QSqlQuery>
#include <QVariant>
#include <QDebug>
int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    bool ok = false;
    { // Destroy all query and database handles before removeDatabase.
        auto db = QSqlDatabase::addDatabase("QSQLITE", "handbook");
        db.setDatabaseName(":memory:");
        if (db.open()) {
            QSqlQuery query(db);
            ok = query.exec("CREATE TABLE sample (id INTEGER PRIMARY KEY)") &&
                 query.prepare("INSERT INTO sample VALUES (?)");
            query.addBindValue(7);
            ok = ok && query.exec() && query.exec("SELECT id FROM sample") &&
                 query.next() && query.value(0).toInt() == 7;
            query.finish();
        }
        db.close();
    }
    QSqlDatabase::removeDatabase("handbook");
    if (!ok) return 1;
    qInfo() << "Qt SQLite memory database OK";
}
