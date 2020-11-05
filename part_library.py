from enum import Enum
from typing import *
from ismt import *

# A library of parts for testing

class PartType(Enum):
    POWER_SUPPLY = 0
    MICROCONTROLLER = 1
    POWER_CONVERTER = 2

class Part:

    def __init__(self, cost:int, footprint: List[Port], part_type:PartType):
        self.cost = cost
        self.footprint = footprint
        self.part_type = part_type

    def get_cost(self) -> int:
        return self.cost




    