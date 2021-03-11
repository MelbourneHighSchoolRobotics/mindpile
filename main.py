import ast
import xml.etree.ElementTree as ET
import Utility.utility as utility
import Parser
from Mapping.utils import generateSetupAST, startCodeGen

tree = ET.parse("TestInputs\/basic\/Program.ev3p")
root = tree.getroot()
xmlstr = ET.tostring(root, encoding="utf8", method="xml")

for elem in root.iter(utility.addNameSpace("BlockDiagram")):
    root = elem

# print(root[0])


codeBlock = Parser.tagHandler.translateElementToIRForm(root)
print()
codeBlock.sortInternalFlow()
# print(codeBlock)
# print("\n".join([str(block) for block in inloop]))
startCodeGen()
tree = ast.parse('')
main = codeBlock.toAST()
tree.body += generateSetupAST().body
tree.body.append(main)
tree = ast.fix_missing_locations(tree)
print(ast.unparse(tree))
