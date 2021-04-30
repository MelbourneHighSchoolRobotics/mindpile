from typing import Tuple, List, Optional, Union
import mindpile.IntermediateFormat as IntermediateFormat
from mindpile.Utility.types import *
from mindpile.Utility import utility as utility
from mindpile.Utility import exceptions as exceptions


def getSequenceTerminalInfo(elem: Terminal) -> Tuple[str, Optional[str]]:
    """
    Returns the type of sequence/flow terminal and the wire it attaches to
    """
    wire = None
    if "Wire" in elem.attrib:
        wire = elem.attrib["Wire"]
    if elem.attrib["Id"] == "SequenceIn" or elem.attrib["Direction"] == "Input":
        return "in", wire
    elif elem.attrib["Id"] == "SequenceOut" or elem.attrib["Direction"] == "Output":
        return "out", wire
    else:
        raise NotImplementedError(
            "Encountered Unexpected Bare terminal in method call", elem
        )


def getTerminalsFromParentElem(elem) -> Tuple[Optional[str],Optional[str]]:
    seqIn,seqOut = None,None
    for child in elem:
        tag = utility.removeNameSpace(child.tag)
        if tag == "Terminal":
            direction, wire = getSequenceTerminalInfo(child)
            if direction == "in":
                seqIn = wire
            else:
                seqOut = wire
    if seqIn == None and seqOut == None:
        raise exceptions.InvalidSourceFormatError("Expected a Terminal where none existed")
    return seqIn,seqOut

def whileLoop(elem: WhileLoop) -> IntermediateFormat.SequenceBlock:
    childBlocks: List[IntermediateFormat.SequenceBlock] = []
    seqIn: Optional[str] = None
    seqOut: Optional[str] = None
    seqIn, seqOut = getTerminalsFromParentElem(elem)
    for child in elem:
        tag = utility.removeNameSpace(child.tag)
        if tag == "ConfigurableWhileLoop.BuiltInMethod":
            if child.attrib["CallType"] == "LoopIndex":
                childBlocks.append(methodCall(child[0]))
            else:
                childBlocks.append(
                    methodCall(child[0], isBreakMethod=True)
                )  # normally we can just use the generic translater, but here we want to make sure the break method is known to be a break method, so we bypass that to pass the flag
        else:
            childBlocks.append(translateElementToIRForm(child))

    label = elem.attrib["InterruptName"]
    loop = IntermediateFormat.WhileLoop(label, childBlocks)
    return IntermediateFormat.SequenceBlock(elem.attrib["Id"], seqIn, seqOut, loop)


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


def methodCall(
    elem: MethodCall, isBreakMethod=False, isWaitForMethod=False
) -> IntermediateFormat.SequenceBlock:

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
            else:  # is outpu [0].attrib["Direction"] == "Output"t
                outputs.append(configureableMethodTerminal(IO))
        elif tag == "Terminal":
            dir, wire = getSequenceTerminalInfo(IO)
            if dir == "in":
                seqInputWire = wire
            else:
                seqOutputWire = wire
        else:
            raise NotImplementedError("Unexpected tag in method call")
    if isBreakMethod:
        method = IntermediateFormat.BreakMethodCall(functionName, arguments, outputs)
    elif isWaitForMethod:
        method = IntermediateFormat.WaitForMethodCall(functionName, arguments, outputs)
    else:
        method = IntermediateFormat.MethodCall(functionName, arguments, outputs)

    return IntermediateFormat.SequenceBlock(
        elem.attrib["Id"], seqInputWire, seqOutputWire, method
    )

def configurableWaitForMethodCall(elem: MethodCall):
    return methodCall(elem, isWaitForMethod=True)

# THIS IS HARDCODED - unsure if this will prove problematic
def startBlock(elem):
    outputWire = elem[1].attrib["Wire"]  # this is the terminal output
    return IntermediateFormat.SequenceBlock(elem.attrib["Id"], None, outputWire, None)


def blockDiagram(elem):
    return IntermediateFormat.BlockDiagram(
        elem.attrib["Name"], [translateElementToIRForm(child) for child in elem]
    )


def configurableFlatCaseStructure(elem):
    seqIn, seqOut = getTerminalsFromParentElem(elem)

    cases = []
    for child in elem:
        tag = utility.removeNameSpace(child.tag)
        if tag == "ConfigurableFlatCaseStructure.Case":
            caseChildren = []
            for child2 in child:
                caseChildren.append(translateElementToIRForm(child2))
            newCase = IntermediateFormat.Case(child.attrib["Id"],child.attrib["Pattern"],caseChildren)
            cases.append(newCase)
    defaultCaseId = elem.attrib["Default"]
    switch = IntermediateFormat.SwitchCase(
        elem.attrib["Id"],
        elem.attrib["DataType"],
        elem.attrib["PairedConfigurableMethodCall"],
        cases,
        defaultCaseId
    )
    return IntermediateFormat.SequenceBlock(elem.attrib["Id"],seqIn,seqOut,switch)

#ok
#so basically
#we enter the paired method
#the value is computed
#then we enter the switch
#and that happens /IMPLICITLY/

def pairedMethodCall(elem:PairedConfigurableMethodCall):
    methodBlock = methodCall(elem) #reuse logic from method call, then extract data into proper sequenceblock
    innerMethod = methodBlock.logic
    pairedMethod = IntermediateFormat.PairedMethodCall(innerMethod,elem.attrib["PairedStructure"])

    return IntermediateFormat.SequenceBlock(methodBlock.id,methodBlock.inputWire,methodBlock.outputWire,pairedMethod)


def sequenceNode(elem:SequenceNode):
    seqIn, seqOut = getTerminalsFromParentElem(elem)
    return IntermediateFormat.SequenceBlock(elem.attrib["Id"],seqIn,seqOut,None)

def translateElementToIRForm(elem):
    tagToIRFunc = {
        "ConfigurableMethodCall": methodCall,
        "ConfigurableWhileLoop": whileLoop,
        "StartBlock": startBlock,
        "BlockDiagram": blockDiagram,
        "ConfigurableWaitFor": configurableWaitForMethodCall,
        "PairedConfigurableMethodCall": pairedMethodCall,  # TODO check this probably needs special handling for the paired swich
        "ConfigurableFlatCaseStructure": configurableFlatCaseStructure,
        "Terminal": lambda x: "Terminal??",  # these need to be handled appropriately
        "ConfigurableWhileLoop.BuiltInMethod": lambda x: "",
        "SequenceNode": sequenceNode,
        "Wire": lambda x: IntermediateFormat.SequenceBlock(
            "DEBUG NOT USED", "DEBUG NOT USED", "DEBUG DONT USE", None
        ),
    }
    return tagToIRFunc[utility.removeNameSpace(elem.tag)](elem)

