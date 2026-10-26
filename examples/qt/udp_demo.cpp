#include <QCoreApplication>
#include <QUdpSocket>
#include <QHostAddress>
#include <QDebug>
int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    QUdpSocket receiver, sender;
    if (!receiver.bind(QHostAddress(QHostAddress::LocalHost), 0)) return 1;
    const QByteArray payload("sample=7");
    if (sender.writeDatagram(payload, QHostAddress::LocalHost, receiver.localPort()) != payload.size()) return 2;
    if (!receiver.hasPendingDatagrams() && !receiver.waitForReadyRead(1000)) return 3;
    const auto size = receiver.pendingDatagramSize();
    if (size < 0 || size > 1024) return 4;
    QByteArray received(static_cast<int>(size), '\0');
    QHostAddress peer;
    quint16 port = 0;
    if (receiver.readDatagram(received.data(), received.size(), &peer, &port) != size) return 5;
    if (!peer.isLoopback() || port != sender.localPort() || received != payload) return 6;
    qInfo() << "UDP loopback OK";
}
