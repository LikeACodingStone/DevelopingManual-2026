#include <QCoreApplication>
#include <QThread>
#include <QTimer>
#include <QDebug>
#include <atomic>
int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    QThread thread;
    auto *worker = new QObject;
    std::atomic<bool> correct{false};
    worker->moveToThread(&thread);
    QObject::connect(&thread, &QThread::started, worker, [&] {
        correct.store(QThread::currentThread() == &thread);
        thread.quit();
    }, Qt::QueuedConnection);
    QObject::connect(&thread, &QThread::finished, worker, &QObject::deleteLater);
    QObject::connect(&thread, &QThread::finished, &app, &QCoreApplication::quit);
    QTimer::singleShot(2000, &app, [&] { thread.quit(); app.exit(2); });
    thread.start();
    int result = app.exec();
    thread.quit();
    thread.wait(); // Worker contains no blocking I/O; arbitrary workers need cooperative cancellation.
    if (result || !correct.load()) return 1;
    qInfo() << "Qt worker thread and shutdown OK";
}
