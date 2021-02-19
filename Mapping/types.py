from abc import ABC, abstractmethod
from typing import Any

class EV3Type(ABC):
    @staticmethod
    @abstractmethod
    def parse(input: str) -> Any:
        pass

class InPort(EV3Type):
    @staticmethod
    def parse(input: str):
        # Convert "1.A" -> "inA"
        # TODO: EV3 allows selecting ports from other paired bricks (specified by the number)
        return "in" + input[2]

class OutPort(EV3Type):
    @staticmethod
    def parse(input: str):
        # Convert "1.A" -> "outA"
        # TODO: EV3 allows selecting ports from other paired bricks (specified by the number)
        return "out" + input[2]
