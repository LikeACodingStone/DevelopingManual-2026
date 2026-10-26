QT += core
QT -= gui
CONFIG += console c++11
CONFIG -= app_bundle
TEMPLATE = app
TARGET = serial_demo
SOURCES += serial_demo.cpp
# External installed dependency: header/library directories supplied via qmake arguments.
INCLUDEPATH += $$QEXT_INCLUDE
LIBS += -L$$QEXT_LIB -lqextserialport
