from Utility.types import *
from Utility import utility as utility
import IntermediateFormat
from typing import Tuple, List, Optional, Union


def getSequenceTerminalInfo(elem: Terminal) -> Tuple[str, Optional[str]]:
    """
    Returns the type of sequence/flow terminal and the wire it attaches to
    """
    wire = None
    if "Wire" in elem.attrib:
        wire = elem.attrib["Wire"]
    if elem.attrib["Id"] == "SequenceIn":
        return "in", wire
    elif elem.attrib["Id"] == "SequenceOut":
        return "out", wire
    else:
        raise NotImplementedError(
            "Encountered Unexpected Bare terminal in method call", elem
        )


def whileLoop(elem: WhileLoop) -> IntermediateFormat.SequenceBlock:
    childBlocks: List[IntermediateFormat.SequenceBlock] = []
    seqIn: Optional[str] = None
    seqOut: Optional[str] = None

    # this could be changed to a special representation, not sure - TODO
    indexMethod: Optional[IntermediateFormat.SequenceBlock] = None
    stopMethod: Optional[IntermediateFormat.SequenceBlock] = None

    for child in elem:
        tag = utility.removeNameSpace(child.tag)
        if tag == "Terminal":
            direction, wire = getSequenceTerminalInfo(child)
            if direction == "in":
                seqIn = wire
            else:
                seqOut = wire
        elif tag == "ConfigurableWhileLoop.BuiltInMethod":
            if child.attrib["CallType"] == "LoopIndex":
                indexMethod = methodCall(child[0])
            else:
                stopMethod = methodCall(child[0])
        else:
            childBlocks.append(translateElementToIRForm(child))

    loop = IntermediateFormat.WhileLoop(indexMethod, stopMethod, childBlocks)
    return IntermediateFormat.SequenceBlock(seqIn, seqOut, loop)


def configureableMethodTerminal(
    elem: ConfigurableMethodTerminal,
) -> Union[IntermediateFormat.Argument, IntermediateFormat.Output]:

    terminal = elem[0]
    name = terminal.attrib["Id"]
    dataType = terminal.attrib["DataType"]
    if terminal.attrib["Direction"] == "Output":
        if "Wire" in terminal.attrib:
            return IntermediateFormat.Output(name, dataType, terminal.attrib["Wire"])
        else:
            return IntermediateFormat.Output(name, dataType, None)
    else:
        if "Wire" in terminal.attrib:
            return IntermediateFormat.Argument(
                name, dataType, variableName=terminal.attrib["Wire"]
            )
        else:
            return IntermediateFormat.Argument(
                name, dataType, constValue=elem.attrib["ConfiguredValue"]
            )


def methodCall(elem: MethodCall) -> IntermediateFormat.SequenceBlock:

    functionName = elem.attrib["Target"]

    seqInputWire = None
    seqOutputWire = None
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
            dir, wire = getSequenceTerminalInfo(IO)
            if dir == "in":
                seqInputWire = wire
            else:
                seqOutputWire = wire
        else:
            raise NotImplementedError("Unexpected tag in method call")

    method = IntermediateFormat.MethodCall(functionName, arguments, outputs)

    return IntermediateFormat.SequenceBlock(seqInputWire, seqOutputWire, method)


# THIS IS HARDCODED - unsure if this will prove problematic
def startBlock(elem):
    outputWire = elem[1].attrib["Wire"]  # this is the terminal output
    return IntermediateFormat.SequenceBlock(None, outputWire, None)


def blockDiagram(elem):
    return IntermediateFormat.BlockDiagram(
        elem.attrib["Name"], [translateElementToIRForm(child) for child in elem]
    )


def translateElementToIRForm(elem):
    tagToIRFunc = {
        "ConfigurableMethodCall": methodCall,
        "ConfigurableWhileLoop": whileLoop,
        "StartBlock": startBlock,
        "BlockDiagram": blockDiagram,
        "Terminal": lambda x: "Terminal??",  # these need to be handled appropriately
        "ConfigurableWhileLoop.BuiltInMethod": lambda x: "",
        "Wire": lambda x: "",
    }
    return tagToIRFunc[utility.removeNameSpace(elem.tag)](elem)

