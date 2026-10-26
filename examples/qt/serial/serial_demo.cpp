// Legacy QextSerialPort 1.2 API: read only; opening may still change device line state.
#include <QCoreApplication>
#include <QTimer>
#include <QDebug>
#include <qextserialport.h>
int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    if (app.arguments().size() != 3 || app.arguments().at(1) != "--read-device") {
        qInfo() << "No device opened. Usage: serial_demo --read-device DEVICE";
        return 0;
    }
    QextSerialPort port(app.arguments().at(2), QextSerialPort::EventDriven);
    port.setBaudRate(BAUD9600);
    port.setDataBits(DATA_8);
    port.setParity(PAR_NONE);
    port.setStopBits(STOP_1);
    port.setFlowControl(FLOW_OFF);
    QObject::connect(&port, &QIODevice::readyRead, &app, [&] {
        qInfo() << "received bytes:" << port.readAll().size();
    });
    if (!port.open(QIODevice::ReadOnly)) return 1;
    QTimer::singleShot(2000, &app, &QCoreApplication::quit);
    const int result = app.exec();
    port.close();
    return result;
}
