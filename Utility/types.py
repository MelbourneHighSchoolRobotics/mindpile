import xml.etree.ElementTree as ET
from typing import NewType

MethodCall = NewType("MethodCall", ET.Element)
ConfigurableMethodTerminal = NewType("ConfigurableMethodTerminal", ET.Element)
MethodTerminal = NewType("MethodTerminal", ET.Element)
WhileLoop = NewType("WhileLoop", ET.Element)
Terminal = NewType("Terminal", ET.Element)
PairedConfigurableMethodCall = NewType("PairedConfigurableMethodCall",ET.Element)
SequenceNode = NewType("PairedConfigurableMethodCall",ET.Element)