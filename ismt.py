from collections import namedtuple
from typing import *
from z3 import *

# Simple circuit constraint satisfaction using Z3 solver
# We want to:
#   (1) Resolve operating limit constraints
#   (2) Ensure connections are well-defined
#       a) Both left and right port exist 
#       b) 1 port is the source and 1 port is the sink
#   (3) Possibly handle ambiguous / unassigned variables?

CircuitVal = namedtuple('CircuitVal', ['current', 'voltage'])


class Port:
    def __init__(self, min_val:CircuitVal, max_val:CircuitVal, preset_value:Optional[CircuitVal] = None, 
                    is_source:bool = True, is_destination:bool = True):
        self.min_val = min_val
        self.max_val = max_val
        self.preset_value = preset_value
        self.is_source = is_source # source / dest == true iff port is copper wire
        self.is_destination = is_destination

class Connection:
    def __init__(self, cid:int, left_port:Port, right_port:Port):
        self.cid = cid
        self.left_port = left_port
        self.right_port = right_port
        self.assigned_val:Optional[CircuitVal] = None # assignment from z3



def make_constraint_from_connection(connection : Connection) -> z3.Bool:  
    '''
    Given a connection, make a Z3 constraint.
    
    Examples:

    '''
    pass

