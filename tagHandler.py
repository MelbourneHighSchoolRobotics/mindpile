import utility
from instructionTypes import *


def whileLoop(elem: WhileLoop):
    return "While loop"


def terminal(elem: Terminal):
    wire = "Unattached"
    if "Wire" in elem.attrib:
        wire = elem.attrib["Wire"]
    return "Terminal, {direction}, {wire}, {dataType}".format(
        direction=elem.attrib["Direction"], wire=wire, dataType=elem.attrib["DataType"]
    )


def methodCall(elem: MethodCall):
    return "Method call: {target}".format(target=elem.attrib["Target"])


def handleElement(elem):
    tag = utility.removeNameSpace(elem.tag)

    if tag == "ConfigurableMethodCall":
        return methodCall(elem)
    elif tag == "ConfigurableWhileLoop":
        return whileLoop(elem)
    elif tag == "Terminal":
        return terminal(elem)
    else:
        return tag

