// Independently written for TinyXML 2.6 API (not TinyXML2).
#include <tinyxml.h>
#include <iostream>
int main() {
    TiXmlDocument doc;
    doc.Parse("<sample channel='7'/>");
    int channel = 0;
    if (doc.Error() || !doc.RootElement() ||
        doc.RootElement()->QueryIntAttribute("channel", &channel) != TIXML_SUCCESS ||
        channel != 7) return 1;
    TiXmlDocument bad;
    bad.Parse("<sample>");
    if (!bad.Error()) return 2;
    std::cout << "TinyXML parse and malformed input OK\n";
}
