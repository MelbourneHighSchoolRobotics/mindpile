from typing import List, Optional
import Utility
from abc import abstractmethod
import copy

# ----------------Metaclasses/interfaces-----------#


class MultiBlockContainer:
    def sortInternalFlow(self):

        # This function propogates changes down the tree in an extremely mutable way. I'm not sure if this is the best way to do this, or if I should just make deep copy of the tree.
        # I'm leaving it like this as a V1 type thing, but it might cause issues down the track.
        inWireToBlock = {}
        for childBlock in self.children:
            inWireToBlock[childBlock.inputWire] = childBlock
        sortedBlocks = []
        currBlock = inWireToBlock[None]
        sortedBlocks.append(currBlock)
        if isinstance(
            childBlock.logic, MultiBlockContainer
        ):  # dislike the code reuse here, it's fine though
            childBlock.logic.sortInternalFlow()
        while True:
            currBlock = inWireToBlock[currBlock.outputWire]
            if isinstance(
                currBlock.logic, MultiBlockContainer
            ):  # propogate the sorting down the tree
                currBlock.logic.sortInternalFlow()
            sortedBlocks.append(currBlock)
            if currBlock.outputWire == None:
                break
        self.children = sortedBlocks

    @property
    @abstractmethod
    def children(self):
        pass

    @children.setter
    @abstractmethod
    def children(self, value):
        pass


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
            name=self.name.replace("\\ ", "_"),
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
            name=self.name.split("\\.vix")[0],
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
class WhileLoop(MultiBlockContainer):
    """
    Intermediate stresntation of the special while loop
    """

    def __init__(self, childInstructions):
        super().__init__()
        self._childInstructions = childInstructions

    def __str__(self):
        whileString = """{blocks}""".format(
            blocks=Utility.utility.addSpacing(
                0, "\n".join([str(command) for command in self._childInstructions])
            ),
        )
        return """While True:\n{whileString}""".format(
            whileString=Utility.utility.addSpacing(4, whileString)
        )

    @property
    def children(self):
        return self._childInstructions

    @children.setter
    def children(self, value):
        self._childInstructions = value


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
        return self.__minRep__()
        return """Block id:{id}| In: {input}, Out: {output}:\n{logic}""".format(
            id=self.id,
            input=self.inputWire,
            output=self.outputWire,
            logic=Utility.utility.addSpacing(4, str(self.logic)),
        )

    def __minRep__(self):
        return f"{self.logic}"

    def __repr__(self):
        return f"<SequenceBlock({self.id},{self.inputWire},{self.outputWire},{self.logic})>"


class BlockDiagram(MultiBlockContainer):
    """
    Container of a whole segment of code
    """

    def __init__(self, name, childInstructions: List[SequenceBlock]):
        super().__init__()
        self.name = name
        self._childInstructions = childInstructions

    def __str__(self):
        return "Start code block {name}:\n{code}".format(
            name=self.name,
            code=Utility.utility.addSpacing(
                4, "\n".join([str(command) for command in self._childInstructions])
            ),
        )

    @property
    def children(self):
        return self._childInstructions

    @children.setter
    def children(self, value):
        self._childInstructions = value
