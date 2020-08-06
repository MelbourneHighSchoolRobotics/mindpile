import utility
from instructionTypes import *
import intermediateFormat


def whileLoop(elem: WhileLoop):
    return "While loop"


def configureableMethodTerminal(elem):
    terminal = elem[0]
    name = terminal.attrib["Id"]
    dataType = terminal.attrib["DataType"]
    if terminal.attrib["Direction"] == "Output":
        if "Wire" in terminal.attrib:
            return intermediateFormat.Output(name, dataType, terminal.attrib["Wire"])
        else:
            return intermediateFormat.Output(name, dataType, None)
    else:
        if "Wire" in terminal.attrib:
            return intermediateFormat.Argument(
                name, dataType, variableName=terminal.attrib["Wire"]
            )
        else:
            return intermediateFormat.Argument(
                name, dataType, constValue=elem.attrib["ConfiguredValue"]
            )


def methodCall(elem: MethodCall):

    functionName = elem.attrib["Target"]

    seqInputWire = ""
    seqOutputWire = ""
    arguments = []
    outputs = []
    for IO in elem:
        tag = utility.removeNameSpace(IO.tag)
        if tag == "ConfigurableMethodTerminal":
            if IO[0].attrib["Direction"] == "Input":
                arguments.append(configureableMethodTerminal(IO))
            else:  # is output
                outputs.append(configureableMethodTerminal(IO))
        elif tag == "Terminal":
            if IO.attrib["Id"] == "SequenceIn":
                seqInputWire = IO.attrib["Id"]
            elif IO.attrib["Id"] == "SequenceOut":
                seqInputWire = IO.attrib["Id"]
            else:
                raise NotImplementedError(
                    "Encountered Unexpected Bare terminal in method call"
                )
        else:
            raise NotImplementedError("Unexpected tag in method call")

    method = intermediateFormat.MethodCall(functionName, arguments, outputs)

    return intermediateFormat.SequenceBlock(seqInputWire, seqOutputWire, method)


def handleElement(elem):
    tag = utility.removeNameSpace(elem.tag)

    if tag == "ConfigurableMethodCall":
        return methodCall(elem)
    elif tag == "ConfigurableWhileLoop":
        return whileLoop(elem)
    elif tag == "ConfigurableMethodTerminal":
        return ""
    elif tag == "Terminal":
        return ""
    else:
        return tag

