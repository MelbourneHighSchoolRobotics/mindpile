import xml.etree.ElementTree as ET
import Utility.utility as utility
import Parser

tree = ET.parse("TestInputs\/switchnumeric\/Program.ev3p")
root = tree.getroot()
xmlstr = ET.tostring(root, encoding="utf8", method="xml")

for elem in root.iter(utility.addNameSpace("BlockDiagram")):
    root = elem

# print(root[0])


codeBlock = Parser.tagHandler.translateElementToIRForm(root)
IdMapping = codeBlock.getBlockIdMapping()
WireMapping = codeBlock.getInWireMapping()
print(IdMapping)
print(WireMapping)
print()
codeBlock.sortInternalFlow()
print(codeBlock)
# print("\n".join([str(block) for block in inloop]))

