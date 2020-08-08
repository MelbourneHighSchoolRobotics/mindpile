from typing import List, Optional
import Utility

# ------------- Methods --------------------------#


class Argument:
    """
    Intermediate stresentation of arugments to method calls
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

    def __str__(self):
        return "{name}={value}".format(
            name=self.name,
            value=self.variableName if self.variableName != None else self.constValue,
        )


class Output:
    """
    Intermediate stresentation of Outputs from method calls, and the variables (wires) they are assigned to
    """

    def __init__(self, name: str, type: str, variableName: str):
        self.name = name
        self.type = type
        self.variableName = variableName

    def __str__(self):
        return "{variableName} = {name}".format(
            variableName=self.variableName, name=self.name
        )

    def __repr__(self):
        return f"<Output({self.name},{self.type},{self.variableName})>"


class MethodCall:
    """
    Intermediate stresentation of the methods that are called. This is the vast majority of mindstorms blocks - sensors, motors
    """

    def __init__(self, name: str, arguments: List[Argument], outputs: List[Output]):
        self.name = name
        self.arguments = arguments
        self.outputs = outputs

    def __str__(self):
        return "{name}({arguments}) -> {outputs}".format(
            name=self.name.split("\\")[0],
            arguments=",".join([str(arg) for arg in self.arguments]),
            outputs=self.outputs,
        )


class BreakMethodCall(MethodCall):
    def __init__(self, name, arguments, outputs):
        super().__init__(name, arguments, outputs)

    def __str__(self):
        args = ",".join([str(arg) for arg in self.arguments])
        return f"if {self.name}({args}) -> {self.outputs}:\n    break"


# ------------------------- end method parts ------------------
# TODO figure out all the possibilities for while loop configs
class WhileLoop:
    """
    Intermediate stresntation of the special while loop
    """

    def __init__(self, blocks):
        self.blocks = blocks

    def __str__(self):
        whileString = """do:\n{blocks}""".format(
            blocks=Utility.utility.addSpacing(
                4, "\n".join([str(command) for command in self.blocks])
            ),
        )
        return """While True:\n{whileString}""".format(
            whileString=Utility.utility.addSpacing(4, whileString)
        )


# THIS IS NOT DONE, DO NOT USE
class SwitchCase:
    def __init__(self, id, dataType, pairedMethodId, actions, inputWire, outputWire):
        self.id = id
        self.dataType = dataType
        self.pairedMethodId = pairedMethodId

    def __str__(self):
        pass


class SequenceBlock:
    """
    Interemediate stresentation of sequences. All blocks have terminals which dictate the flow of logic. This codifies that concept
    """

    def __init__(self, id, inputWire, outputWire, logic):
        self.inputWire = inputWire
        self.outputWire = outputWire
        self.logic = logic
        self.id = id

    def __str__(self):
        return """Block id:{id}| In: {input}, Out: {output}:\n{logic}""".format(
            id=self.id,
            input=self.inputWire,
            output=self.outputWire,
            logic=Utility.utility.addSpacing(4, str(self.logic)),
        )

    def __repr__(self):
        return f"<SequenceBlock({self.id},{self.inputWire},{self.outputWire},{self.logic})>"


class BlockDiagram:
    """
    Container of a whole segment of code
    """

    def __init__(self, name, logic: List[SequenceBlock]):
        self.name = name
        self.logic = logic

    def __str__(self):
        return "Start code block {name}:\n{code}".format(
            name=self.name,
            code=Utility.utility.addSpacing(
                4, "\n".join([str(command) for command in self.logic])
            ),
        )

