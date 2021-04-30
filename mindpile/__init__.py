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

def from_ev3(ev3_path):
    import os
    import tempfile
    from zipfile import ZipFile
    # Some preliminary checks
    if not ev3_path.endswith(".ev3"):
        raise ValueError("The mindstorms file to extract should have the `.ev3` file ending.")
    # First -> Unzip the .ev3 file into a temporary location. Extract the ev3p file.
    with tempfile.TemporaryDirectory() as tmpdir:
        with ZipFile(ev3_path, "r") as zipObj:
            zipObj.extractall(tmpdir)
        # Second -> Generate the python code.
        python_source = to_python(os.path.join(tmpdir, "Program.ev3p"))
        return python_source