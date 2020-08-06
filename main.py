import xml.etree.ElementTree as ET
import Utility.utility as utility
import Parser

tree = ET.parse("TestInputs\/Program.ev3p")
root = tree.getroot()
xmlstr = ET.tostring(root, encoding="utf8", method="xml")

for elem in root.iter(utility.addNameSpace("BlockDiagram")):
    root = elem

print(root[0])
print(Parser.tagHandler.translateElementToIRForm(root[1]))
