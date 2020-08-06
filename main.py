import xml.etree.ElementTree as ET
import utility
import tagHandler

tree = ET.parse("Program.ev3p")
root = tree.getroot()
xmlstr = ET.tostring(root, encoding="utf8", method="xml")


def prettyPrint(depthInfoTree):
    print(depthInfoTree[0] * "    ", end="")

    print(tagHandler.handleElement(depthInfoTree[1]))

    for child in depthInfoTree[2]:
        prettyPrint(child)


for elem in root.iter(utility.addNameSpace("BlockDiagram")):
    root = elem

prettyPrint(utility.getDepthInfoTree(root))
