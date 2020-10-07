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
    def __init__(self, min_val:CircuitVal, max_val:CircuitVal, port_type:PortType, 
                    preset_value:Optional[CircuitVal] = None):
        # assert min_val < max_val?
        self.min_val = min_val
        self.max_val = max_val
        self.port_type = port_type
        self.preset_value = preset_value

    def __str__(self):
        return "[min:" + str(self.min_val) + ", max:" + str(self.max_val) + "]"

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
        return str(self.cid) + ":" + str(self.left_port) + ", " + str(self.right_port)

#@TODO REDO THIS
def intervals_overlap(lp: Port, rp: Port) -> Bool:
    current_overlap:bool = lp.min_val.current <= rp.max_val.current and rp.min_val.current <= lp.min_val.current
    voltage_overlap:bool = lp.min_val.voltage <= rp.max_val.voltage and rp.min_val.voltage <= lp.min_val.voltage

    return current_overlap and voltage_overlap

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

    # (Source) -> https://nedbatchelder.com/blog/201310/range_overlap_in_two_compares.html
    overlap_constraint : bool = intervals_overlap(left_port, right_port)
    port_sink_constraint : bool = connection.valid_source_sink()

    return (overlap_constraint) and (port_sink_constraint)

def design_is_sat(design : List[Connection]) -> bool:
    '''
    Given a design as a list of connections, sat it
    '''
    constraints = map(make_constraint_from_connection, design)
    return all(constraints)