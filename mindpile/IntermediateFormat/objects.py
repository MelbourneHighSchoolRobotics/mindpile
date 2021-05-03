import ast
import re
from abc import abstractmethod
from typing import List, Optional,Union,Dict
import mindpile.Utility as Utility
from mindpile.Mapping.types import get_parser
from mindpile.Mapping.utils import methods, newGlobalName
from mindpile.Mapping.types import get_type, get_parser

def to_body_ast(children, ctx={}):
    body = []
    for command in children:
        tree = command.toAST(ctx=ctx)
        if tree is not None:
            if isinstance(tree, ast.AST):
                body.append(tree)
            elif isinstance(tree, list):
                body += tree
            else:
                # If you got here there's a bug in a toAST()
                raise Exception("How did you get here?")
    if len(body) == 0:
        body.append(ast.Pass())
    return body

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

    @staticmethod
    def toString(name, arguments, outputs):
        return "{name}({arguments}) -> {outputs}".format(
            name=name.split("\\.vix")[0],
            arguments=",".join([str(arg) for arg in arguments]),
            outputs=outputs,
        )
    
    def __str__(self):
        return MethodCall.toString(self.name, self.arguments, self.outputs)
    
    @staticmethod
    def stripArgumentName(name):
        return re.sub(r'\W+', '', name) # Strip all non-alphanumeric from argument name

    @staticmethod
    def toMethodAST(name, arguments, outputs, ctx={}):
        name = name.replace("\\", "")
        method = methods.get(name)
        if method is None:
            raise Exception(f"Method not implemented: {MethodCall.toString(name, arguments, outputs)}")

        args = {}
        for arg in arguments:
            arg_name = MethodCall.stripArgumentName(arg.name)
            if arg.variableName is None:
                args[arg_name] = arg.constValue
            else:
                args[arg_name] = ast.Name(id=arg.variableName, ctx=ast.Load())
        
        for arg in outputs:
            arg_name = MethodCall.stripArgumentName(arg.name)
            if arg.variableName is None:
                args[arg_name] = ast.Name(id="__void", ctx=ast.Store())
            else:
                args[arg_name] = ast.Name(id=arg.variableName, ctx=ast.Store())

        merged_args = {**args, **ctx}
        tree = method(**merged_args)
        return tree
    
    def toAST(self, ctx={}):
        return MethodCall.toMethodAST(self.name, self.arguments, self.outputs, ctx=ctx)
    
    def setResultVariable(self, newVariable):
        if len(self.outputs) == 1:
            self.outputs[0].variableName = newVariable
            return

        for output in self.outputs:
            if output.name == "Result":
                output.variableName = newVariable
                return


class BreakMethodCall(MethodCall):
    def __init__(self, name, arguments, outputs):
        super().__init__(name, arguments, outputs)

    def __str__(self):
        args = ",".join([str(arg) for arg in self.arguments])
        return f"if {self.name}({args}) -> {self.outputs}:\n    break"
    
    def toAST(self, ctx={}):
        self.setResultVariable("breakCondition")
        tree = [
            super().toAST(ctx=ctx),
            ast.If(
                test=ast.Name(id="breakCondition", ctx=ast.Load()),
                body=[ast.Break()],
                orelse=[]
            )
        ]
        return tree


class WaitForMethodCall(MethodCall):
    def __init__(self, name, arguments, outputs):
        super().__init__(name, arguments, outputs)
    
    def toAST(self, ctx={}):
        wait_enter_time = ast.Name(id=newGlobalName(), ctx=ast.Store())
        
        self.setResultVariable("waitBreakCondition")
        body = super().toAST(ctx={
            **ctx,
            "WaitEnterTime": wait_enter_time,
        })
        tree = [
            ast.Assign(targets=[wait_enter_time], value=(
                ast.Call(func=ast.Attribute(value=ast.Name(id='time', ctx=ast.Load()), attr='time', ctx=ast.Load()), args=[], keywords=[])
            )),
            ast.While(
                test=ast.Constant(True),
                body=[
                    body,
                    ast.If(
                        test=ast.Name(id="waitBreakCondition", ctx=ast.Load()),
                        body=[ast.Break()],
                        orelse=[]
                    )
                ],
                orelse=[]
            )
        ]
        return tree


# ------------------------- end method parts ------------------
# TODO figure out all the possibilities for while loop configs
class WhileLoop(MultiBlockContainer):
    """
    Intermediate stresntation of the special while loop
    """

    def __init__(self, label, childInstructions):
        super().__init__()
        self._label = label
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
    
    def toAST(self, ctx={}):
        loop_iteration_count = ast.Name(id=newGlobalName(), ctx=ast.Store())
        loop_enter_time = ast.Name(id=newGlobalName(), ctx=ast.Store())

        body = to_body_ast(self.children, ctx={
            **ctx,
            "LoopIterationCount": loop_iteration_count,
            "LoopEnterTime": loop_enter_time,
            "LoopLabel": self.label,
        })

        if ctx["ev3sim_support"]:
            body.append(methods["ev3sim_wait_for_tick.vix"]())

        tree = [
            ast.Assign(targets=[loop_iteration_count], value=ast.Constant(value=1)),
            ast.Assign(targets=[loop_enter_time], value=(
                ast.Call(func=ast.Attribute(value=ast.Name(id='time', ctx=ast.Load()), attr='time', ctx=ast.Load()), args=[], keywords=[])
            )),
            ast.While(
                test=ast.Constant(True),
                body=(
                    body + [
                        ast.AugAssign(target=loop_iteration_count, op=ast.Add(), value=ast.Constant(value=1))
                    ]
                ),
                orelse=[]
            )
        ]
        return tree
    
    @property
    def label(self):
        return self._label

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
    def __init__(self, id, dataType:str, pairedMethodId:str, cases:List[Case], defaultCaseId=str):
        self.id = id
        self.dataType = dataType
        self.pairedMethodId = pairedMethodId
        self.cases = cases
        self.defaultCaseId = defaultCaseId
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
    
    def toAST(self, ctx={}):
        switchVar = ast.Name(id="switchVar", ctx=ast.Load())
        type = get_type(self.dataType)
        parser = get_parser(type)

        def compare(value):
            if type == str:
                # Strip out surrounding quotes in strings
                value = value[1:-1]
            value = parser(value)
            v = ast.Constant(value=value)

            if type == int:
                return ast.Compare(
                    left=ast.Call(func=ast.Name(id='int', ctx=ast.Load()), args=[switchVar], keywords=[]),
                    ops=[ast.Eq()],
                    comparators=[v]
                )
            elif type == float:
                return ast.Call(
                    func=ast.Attribute(value=ast.Name(id='math', ctx=ast.Load()), attr='isclose', ctx=ast.Load()),
                    args=[
                        switchVar,
                        v,
                    ],
                    keywords=[]
                )

            return ast.Compare(
                left=switchVar,
                ops=[ast.Eq()],
                comparators=[v]
            )
        
        defaultCase = None
        for case in self.cases:
            if case.id == self.defaultCaseId:
                defaultCase = case
                break
        if type != str and defaultCase.pattern == '"Unused"':
            defaultCase = None

        childCase = None
        for case in reversed(self.cases):
            if case is defaultCase:
                continue
            if type != str and case.pattern == '"Unused"':
                continue

            if childCase is None:
                childCase = ast.If(
                    test=compare(case.pattern),
                    body=to_body_ast(case.children),
                    orelse=[] if defaultCase is None else to_body_ast(defaultCase.children)
                )
            else:
                childCase = ast.If(
                    test=compare(case.pattern),
                    body=to_body_ast(case.children),
                    orelse=[childCase]
                )
        return childCase


class PairedMethodCall:
    def __init__(self,method:MethodCall,pairedSwitchId:str):
        self.method = method
        self.pairedSwitchId = pairedSwitchId
        self.pairedSwitch:Optional['SequenceBlock'] = None
    def __str__(self):
        return f"PairedMethodCall: switchVar = ({self.method})"
    def toAST(self, ctx={}):
        self.method.setResultVariable("switchVar")
        return self.method.toAST(ctx=ctx)

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

    def toAST(self, ctx={}):
        if self.logic is not None:
            return self.logic.toAST(ctx=ctx)
        return None


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
    
    def toAST(self, ctx={}):
        return to_body_ast(self.children, ctx=ctx)

    @property
    def children(self):
        return self._childInstructions

    @children.setter
    def children(self, value):
        self._childInstructions = value
