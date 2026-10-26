#include <QCoreApplication>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonParseError>
#include <QDebug>
int main(int argc, char **argv) {
    QCoreApplication app(argc, argv);
    QJsonParseError error;
    auto doc = QJsonDocument::fromJson(R"({"channel":7,"unit":"V"})", &error);
    if (error.error != QJsonParseError::NoError || !doc.isObject()) return 1;
    auto value = doc.object().value("channel");
    if (!value.isDouble() || value.toDouble() != 7) return 2;
    QJsonDocument::fromJson("{", &error);
    if (error.error == QJsonParseError::NoError) return 3;
    qInfo() << "Qt JSON parse and malformed input OK";
}
