import xml.etree.ElementTree as ET
import utility
import tagHandler

tree = ET.parse("Program.ev3p")
root = tree.getroot()
xmlstr = ET.tostring(root, encoding="utf8", method="xml")

for elem in root.iter(utility.addNameSpace("BlockDiagram")):
    root = elem

print(root[0])
print(tagHandler.translateElementToIRForm(root[1]))
