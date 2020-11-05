from typing import *
from ismt import *
from part_library import *

# Optimizing a solved circuit for part cost
class Circuit:
    def __init__(self, parts: List[Part], connections: List[Connection]):
        self.parts = parts
        self.connections = connections

    def get_parts(self):
        return self.parts

def energy_function(circuit:Circuit) -> int:
    """
    Given a circuit, return it's energy.
    Canonically, lower energy is better
    """
    cost = 0
    for part in circuit.get_parts():
        cost += part.get_cost()
    return cost

def get_neighbor(circuit:Circuit, temperature:int):
    """
    Given a circuit, twiddle it's parts to generate another valid circuit.
    """
    # TODO implement
    # TODO interactivity can go here! User specifies which parts to select next? 
    # or which pool of parts to choose from
    pass

def simulated_annealing(start_state:Circuit, num_iterations:int):
    """
    Given a starting circuit, optimize circuit design for cost.
    """
    # TODO implement
    # TODO user interactivity
    pass
