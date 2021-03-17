from abc import ABC, abstractmethod
from typing import Any

def boolParser(input: str):
    return input == "True"

def get_parser(type):
    parser = None
    if type == int:
        parser = int
    elif type == str:
        parser = str
    elif type == bool:
        parser = boolParser
    elif type == float:
        parser = float
    elif isinstance(type, EV3Type) or issubclass(type, EV3Type):
        parser = type.parse
    return parser

class Local:
    def __init__(self, initial_value) -> None:
        self.initial_value = initial_value

class EV3Type(ABC):
    @staticmethod
    @abstractmethod
    def parse(input: str) -> Any:
        pass

class List(EV3Type):
    def __init__(self, type):
        self.parser = get_parser(type)
        if self.parser is None:
            raise Exception(f"Type {type} is not a supported parameter type")
    
    def parse(self, input: str):
        parser = self.parser
        body = input[1:-1] # Remove surrounding []
        if body == '':
            items_str = []
        else:
            items_str = body.split(',')
        items = list(map(parser, items_str))
        return items

class Literal(EV3Type):
    def __init__(self, type):
        self.parser = get_parser(type)
        if self.parser is None:
            raise Exception(f"Type {type} is not a supported parameter type")
    
    def parse(self, input: str):
        return self.parser(input)

class InPort(EV3Type):
    @staticmethod
    def parse(input: str):
        # Convert "1.4" -> 4
        # TODO: EV3 allows selecting ports from other paired bricks (specified by the number)
        if len(input) > 3:
            return None
        port = input[2]
        return ord(port) - 48

class OutPort(EV3Type):
    @staticmethod
    def parse(input: str):
        # Convert "1.A" -> 1, "1.B" -> 2
        # TODO: EV3 allows selecting ports from other paired bricks (specified by the number)
        if len(input) > 3:
            return None
        port = input[2]
        return ord(port) - 64
