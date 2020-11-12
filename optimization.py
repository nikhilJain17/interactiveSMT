from typing import *
from ismt import *
from part_library import *
import math
import random

# Optimizing a solved circuit for part cost
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
    # But for now, just randomly pick from list of similar parts

    is_sat = False
    new_circuit = circuit
    terminate = 10 # TODO just a hack to make sure we terminate the while loop
    while not is_sat:
        terminate -= 1
        # randomly pick a part to change
        old_part = random.choice(circuit.parts)

        # pick a new part of same footprint / type
        new_part = None
        if old_part.part_type == PartType.POWER_SUPPLY:
            new_part = random.choice(power_supplies)
        elif old_part.part_type == PartType.MICROCONTROLLER:
            new_part = random.choice(cpus)
        else:
            print("Invalid part in get_neighbor():", old_part)

        # replace old connections with new connections
        # TODO this seems like it could be a lot better.

        # Right now, iterate over connections. 
        
        # If we see a port with the same name as a port
        # in the old_part, replace this port with the 
        # same port as the one in the new_part.

        # The unique identifier here is the port name,
        # which means (1) there can't be a clash of names
        # across PartTypes (i.e. cpu and psu can't both have
        # ports named "pwr") and (2) parts of the same "type"
        # need to have the same footprint and port names.
        new_connections = []
        old_connections_to_remove = []
        old_part_portnames = old_part.footprint.keys()

        # Create new connections and tally which old connections need to be replaced
        for connection in circuit.connections:
            if connection.left_port.name in old_part_portnames:
                # we have a connection where the left_port is from the old_part
                new_con = Connection(connection.cid, new_part.footprint[connection.left_port.name], connection.right_port)
                new_connections.append(new_con)
                old_connections_to_remove.append(connection.cid)
            elif connection.right_port.name in old_part_portnames:
                # we have a connection where the right_port is from the old_part
                new_con = Connection(connection.cid, connection.left_port, new_part.footprint[connection.right_port.name])
                new_connections.append(new_con)
                old_connections_to_remove.append(connection.cid)

        # Append the unmodified connections
        new_connections += [con for con in circuit.connections if con.cid not in old_connections_to_remove]
        new_parts = [part for part in circuit.parts if part.name != old_part.name] + [new_part]
        new_circuit = Circuit(parts=new_parts, connections=new_connections)

        print("\n=============\nGetNeighbor: \n")
        print("Old Part:", old_part.name, "New Part:", new_part.name, "\n")
        print(new_circuit)

        # check for sat TODO FIX
        print(new_circuit.is_sat())
        is_sat = (new_circuit.is_sat()) or (terminate < 0)

    return new_circuit

def simulated_annealing(start_state:Circuit, num_iterations:int):
    """
    Given a starting circuit, optimize circuit design for cost.
    """
    # TODO implement
    # TODO user interactivity


    # TODO if you only change one part of the circuit, only SAT that new part. Don't change everything.
    x = start_state
    for _ in range(num_iterations):
        x = get_neighbor(x, 0)

