import ast
import xml.etree.ElementTree as ET
import mindpile.Utility.utility as utility
import mindpile.Parser as Parser
from mindpile.Mapping.utils import generateSetupAST, startCodeGen

__version__ = "0.0.1"

def to_python(ev3p_path):
    tree = ET.parse(ev3p_path)
    root = tree.getroot()

    for elem in root.iter(utility.addNameSpace("BlockDiagram")):
        root = elem

    codeBlock = Parser.tagHandler.translateElementToIRForm(root)
    codeBlock.sortInternalFlow()
    startCodeGen()
    tree = ast.parse('')
    main = codeBlock.toAST(ctx={})
    tree.body += generateSetupAST().body
    tree.body += main
    tree = ast.fix_missing_locations(tree)
    return ast.unparse(tree)