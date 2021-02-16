from typing import List, Optional,Union,Dict
import Utility
from abc import abstractmethod
import copy

# ----------------Metaclasses/interfaces-----------#

class MultiBlockContainer:
    #NOTE: Below is a large set of functions used to resolve flow order into something linear
    #This could be done in two passes, but is instead done in a few
    #this is to reduce complexity
    def getBlockIdMapping(self)->Dict[str,Union['SequenceBlock','SwitchCase']]:
        #get a mapping of all Ids and blocks recursively
        #NOTE: This parses the WHOLE CALL TREE
        idToBlock = {}
        for childBlock in self.children:
            if isinstance(childBlock,SequenceBlock) or isinstance(childBlock,SwitchCase):
                idToBlock[childBlock.id] = childBlock
            if(isinstance(childBlock,MultiBlockContainer)): #todo switchCases may need to be mbcontainers too
                idToBlock = {**idToBlock, **childBlock.getBlockIdMapping()}
        return idToBlock
    
    def getInWireMapping(self)->Dict[Optional[str],'SequenceBlock']:
        #gets a dictionary of program flow/wire orders
        # flow goes None->wX -> wX -> None
        #NOTE: This only parses the current level, and wire ids are level scope
        inWireToBlock = {}
        for childBlock in self.children:
            if isinstance(childBlock,SequenceBlock):
                if isinstance(childBlock.logic,SwitchCase):
                    pass #ignore switchcases as they are not true starting blocks (input = None)
                else:
                    inWireToBlock[childBlock.inputWire] = childBlock

        return inWireToBlock

    def _resolveSwitchCases(self,idMap:Dict[str,Union['SequenceBlock','SwitchCase']]):
        # pairs switch cases and paried methods
        # NOTE: This operates on the current level only
        for childBlock in self.children:
            if(isinstance(childBlock,SequenceBlock) and isinstance(childBlock.logic,PairedMethodCall)):
                method:PairedMethodCall = childBlock.logic
                method.pairedSwitch = idMap[method.pairedSwitchId] #type:ignore 
                pass


    def _sortWireOrder(self,idMap:Dict[str,Union['SequenceBlock','SwitchCase']]):
        inWireToBlock = self.getInWireMapping()
        self._resolveSwitchCases(idMap)
        sortedBlocks = []
        startBlock = inWireToBlock[None]
        
        currentBlock = startBlock
        while True:
            if(isinstance(currentBlock.logic,MultiBlockContainer)):
                currentBlock.logic._sortWireOrder(idMap)
            if(isinstance(currentBlock.logic,SwitchCase)):
                for case in currentBlock.logic.cases:
                    case._sortWireOrder(idMap)
                pass

            sortedBlocks.append(currentBlock)

            if currentBlock.outputWire == None: 
                if(isinstance(currentBlock.logic,PairedMethodCall)):
                    if currentBlock.logic:
                        currentBlock = currentBlock.logic.pairedSwitch #type: ignore
                    else:
                        raise Exception("You shouldn't have gotten here... how??") 
                else:
                    break
                # when you've reached none, you're back to the start
            else:
                currentBlock = inWireToBlock[currentBlock.outputWire]
        self.children = sortedBlocks #type: ignore
    def sortInternalFlow(self):
        idMap = self.getBlockIdMapping()
        self._sortWireOrder(idMap)
 
    @property #type: ignore
    @abstractmethod
    def children(self):
        pass

    @children.setter #type: ignore
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

class Case(MultiBlockContainer):
    def __init__(self,id,pattern,children):
        self.id = id
        self.pattern = pattern
        self._childInstructions = children
    def __str__(self):
        return f"Case({self.pattern})"
    def __repr__(self):
        return self.__str__()
    @property
    def children(self):
        return self._childInstructions

    @children.setter
    def children(self, value):
        self._childInstructions = value


class SwitchCase:
    #TODO handle population of children actions
    def __init__(self, id, dataType:str, pairedMethodId:str, cases:List[Case]):
        self.id = id
        self.dataType = dataType
        self.pairedMethodId = pairedMethodId
        self.cases = cases
    def __str__(self):
        outStr = []
        for i,case in enumerate(self.cases):
            if i == 0:
                outStr.append(f"if switchVar == {str(self.cases[0].pattern)}:")
            else:
                outStr.append(f"elif switchVar == {str(self.cases[i].pattern)}:")
            if self.cases[i].children != None:
                for child in self.cases[i].children:
                    outStr.append(f"    {child}")
            else:
                outStr.append("    pass")
        return '\n'.join(outStr)
        #return f"if SwitchVar == {str(self.cases[0])}:"
        #return f"Switch: {str(self.cases)}"



class PairedMethodCall:
    def __init__(self,method:MethodCall,pairedSwitchId:str):
        self.method = method
        self.pairedSwitchId = pairedSwitchId
        self.pairedSwitch:Optional['SequenceBlock'] = None
    def __str__(self):
        return f"PairedMethodCall: switchVar = ({self.method})"
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
