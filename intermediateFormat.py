from typing import List


class Argument:
    def __init__(self, name, dataType, constValue=None, variableName=None):
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
    def __init__(self, name, type, variableName):
        self.name = name
        self.type = type
        self.variableName = variableName


class MethodCall:
    def __init__(self, name: str, arguments: List[Argument], outputs: List[Output]):
        self.name = name
        self.arguments = arguments
        self.outputs = outputs

    def __repr__(self):
        return "method::{name}({arguments}) -> {outputs}".format(
            name=self.name, arguments=self.arguments, outputs=self.outputs
        )


class SequenceBlock:
    def __init__(self, inputWire, outputWire, logic):
        self.inputWire = inputWire
        self.outputWire = outputWire
        self.logic = logic

    def __repr__(self):
        out = []
        return "Block | In: {input}, Out: {output} \n    {logic}".format(
            input=self.inputWire, output=self.outputWire, logic=self.logic
        )
