from collections import namedtuple
from typing import *
from z3 import *
from enum import Enum


# Simple circuit constraint satisfaction using Z3 solver
# We want to:
#   (1) Resolve operating limit constraints
#   (2) Ensure connections are well-defined
#       a) Both left and right port exist
#       b) 1 port is the source and 1 port is the sink
#   (3) Possibly handle ambiguous / unassigned variables?

CircuitVal = namedtuple('CircuitVal', ['current', 'voltage'])

class PortType(Enum):
    COPPER = 0
    SINK = 1
    SOURCE = 2

class Port:
    def __init__(self, name:str, min_val:CircuitVal, max_val:CircuitVal, port_type:PortType,
                    preset_value:Optional[CircuitVal] = None):
        # assert min_val < max_val?
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.port_type = port_type
        self.preset_value = preset_value

    def __str__(self):
        return "[min:(" + str(self.min_val) + ", max:" + str(self.max_val) + "]"

class Connection:
    def __init__(self, cid:int, left_port:Port, right_port:Port):
        self.cid = cid
        self.left_port = left_port
        self.right_port = right_port

    def has_copper_connection(self) -> bool:
        return (self.left_port.port_type == PortType.COPPER) or (self.right_port.port_type == PortType.COPPER)

    def valid_source_sink(self) -> bool:
        if self.has_copper_connection():
            return True
        else:
            right_to_left = self.left_port.port_type == PortType.SOURCE and self.right_port.port_type == PortType.SINK
            left_to_right = self.right_port.port_type == PortType.SOURCE and self.left_port.port_type == PortType.SINK
            return right_to_left ^ left_to_right

    def __str__(self):
        return str(self.cid) + " = {\n"             \
            + "  l:" + str(self.left_port) + "\n"   \
            + "  r:" + str(self.right_port)

def intervals_overlap(lp: Port, rp: Port) -> Bool:
    current = Real('current')
    voltage = Real('voltage')

    s = Solver()

    s.add(current >= lp.min_val.current, current >= rp.min_val.current, current <= lp.max_val.current, current <= rp.max_val.current)
    s.add(voltage >= lp.min_val.voltage, voltage >= rp.min_val.voltage, voltage <= lp.max_val.voltage, current <= rp.max_val.voltage)

    return s.check() == sat

def make_constraint_from_connection(connection : Connection) -> z3.Bool:
    '''
    Given a connection, make a set of z3 constraints.
    Enforce the following:
        a) circuit_val_constraint := circuit limits have overlap
        b) 1 port, 1 sink
        c) if assigned_val, then check if it works

    Examples:

    '''
    left_port = connection.left_port
    right_port = connection.right_port

    overlap_constraint : bool = intervals_overlap(left_port, right_port)
    port_sink_constraint : bool = connection.valid_source_sink()

    return (overlap_constraint) and (port_sink_constraint)

class PartType(Enum):
    POWER_SUPPLY = 0
    MICROCONTROLLER = 1
    POWER_CONVERTER = 2

class Part:
    def __init__(self, name:str, cost:int, footprint, part_type:PartType):
        self.cost = cost
        self.footprint = footprint # map :: str -> port
        self.part_type = part_type
        self.name = name

    def get_cost(self) -> int:
        return self.cost

    def __str__(self):
        ans = self.name + " = { \n" \
                + "   type = " + str(self.part_type) + "\n" \
                + "   cost = " + str(self.cost) + "\n" \
                + "   footprint = TODO" + "\n" \
                + "}"
        return ans

class Circuit:
    def __init__(self, parts: List[Part], connections: List[Connection]):
        self.parts = parts
        self.connections = connections

    def get_parts(self):
        return self.parts

    def __str__(self):
        result =  " ________________\n"
        result += "| (Parts)        |\n" 
        result += " ––––––––––––––––\n"
        for p in self.parts:
            result += str(p) + "\n"
        result += " ––––––––––––––––\n"
        result += "| (Connections)  |\n"
        result += " ––––––––––––––––\n"
        for c in self.connections:
            result += str(c) + "\n"
        return result

    def is_sat(self) -> bool:
        constraints = map(make_constraint_from_connection, self.connections)
        return all(constraints)
