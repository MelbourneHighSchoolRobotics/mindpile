from typing import List, Optional
import Utility

# ------------- Methods --------------------------#


class Argument:
    """
    Intermediate representation of arugments to method calls
    """

    def __init__(
        self,
        name: str,
        dataType: str,
        constValue: Optional[str] = None,
        variableName: Optional[str] = None,
    ):
        if constValue == None and variableName == None:
            raise ValueError("Argument must have a value or a variable input")
        self.name = name
        self.dataType = dataType
        self.constValue = constValue
        self.variableName = variableName

    def __repr__(self):
        return "arg::{name}:{value}".format(
            name=self.name,
            value=self.variableName if self.variableName != None else self.constValue,
        )


class Output:
    """
    Intermediate representation of Outputs from method calls, and the variables (wires) they are assigned to
    """

    def __init__(self, name: str, type: str, variableName: str):
        self.name = name
        self.type = type
        self.variableName = variableName

    def __repr(self):
        return "Out::{variableName} = {name}".format(
            variableName=self.variableName, name=self.name
        )


class MethodCall:
    """
    Intermediate representation of the methods that are called. This is the vast majority of mindstorms blocks - sensors, motors
    """

    def __init__(self, name: str, arguments: List[Argument], outputs: List[Output]):
        self.name = name
        self.arguments = arguments
        self.outputs = outputs

    def __repr__(self):
        return "method::{name}({arguments}) -> {outputs}".format(
            name=self.name, arguments=self.arguments, outputs=self.outputs
        )


# ------------------------- end method parts ------------------
# TODO figure out all the possibilities for while loop configs
class WhileLoop:
    """
    Intermediate represntation of the special while loop
    """

    def __init__(self, indexMethod, stopMethod, blocks):
        self.indexMethod = indexMethod
        self.stopMethod = stopMethod
        self.blocks = blocks

    def __repr__(self):
        return """
        While:: not stop: {stopMethod} \n
            index:{indexMethod} \n
            and do: {blocks}\
        """.format(
            stopMethod=self.stopMethod, indexMethod=self.indexMethod, blocks=self.blocks
        )


class SequenceBlock:
    """
    Interemediate representation of sequences. All blocks have terminals which dictate the flow of logic. This codifies that concept
    """

    def __init__(self, inputWire, outputWire, logic):
        self.inputWire = inputWire
        self.outputWire = outputWire
        self.logic = logic

    def __repr__(self):
        return """Block | In: {input}, Out: {output}:
            {logic}
            """.format(
            input=self.inputWire,
            output=self.outputWire,
            logic=Utility.utility.addSpacing(4, repr(self.logic)),
        )

