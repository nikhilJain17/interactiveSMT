from enum import Enum
from typing import *
from ismt import *

# A library of parts for testing

# Power supplies
psu_positive_terminal = Port(name="psu_positive",       
                            min_val=CircuitVal(0.01, 2.4), 
                            max_val=CircuitVal(10, 7), 
                            port_type=PortType.SOURCE)

psu_negative_terminal = Port(name="psu_negative",
                            min_val=CircuitVal(0.01, -7), 
                            max_val=CircuitVal(10, 0), 
                            port_type=PortType.SINK)

psu_footprint = {}
psu_footprint[psu_positive_terminal.name] = psu_positive_terminal
psu_footprint[psu_negative_terminal.name] = psu_negative_terminal

psu_positive_terminal2 = Port(name="psu_positive",       
                            min_val=CircuitVal(0, 2.4), 
                            max_val=CircuitVal(6, 7), 
                            port_type=PortType.SOURCE)

psu_negative_terminal2 = Port(name="psu_negative",
                            min_val=CircuitVal(0, -5), 
                            max_val=CircuitVal(5, 0), 
                            port_type=PortType.SINK)

psu_footprint2 = {}
psu_footprint2[psu_positive_terminal2.name] = psu_positive_terminal2
psu_footprint2[psu_negative_terminal2.name] = psu_negative_terminal2


cheap_psu = Part(name="cheap_psu", 
                    cost=1, 
                    footprint=psu_footprint,
                    part_type=PartType.POWER_SUPPLY)

middle_psu = Part(name="middle_psu", 
                    cost=10, 
                    footprint=psu_footprint2,
                    part_type=PartType.POWER_SUPPLY)

expensive_psu = Part(name="expensive_psu", 
                    cost=100, 
                    footprint=psu_footprint,
                    part_type=PartType.POWER_SUPPLY)

# TODO implement
unsat_psu = Part(name="unsat_psu", 
                    cost=100, 
                    footprint=None, # <-- TODO implement
                    part_type=PartType.POWER_SUPPLY)


power_supplies = [cheap_psu, middle_psu, expensive_psu]

# CPUs
cpu_power = Port(name="cpu_power",
                    min_val=CircuitVal(0.4, 4), 
                    max_val=CircuitVal(0.6, 5), 
                    port_type=PortType.SINK)

cpu_gnd = Port(name="cpu_ground",
                min_val=CircuitVal(0.4, -0.1), 
                max_val=CircuitVal(0.6, 0.1), 
                port_type=PortType.SINK)

cpu_footprint = {}
cpu_footprint[cpu_power.name] = cpu_power
cpu_footprint[cpu_gnd.name] = cpu_gnd

cpu_power2 = Port(name="cpu_power",
                    min_val=CircuitVal(0.3, 4.5), 
                    max_val=CircuitVal(0.7, 8), 
                    port_type=PortType.SINK)

cpu_gnd2 = Port(name="cpu_ground",
                min_val=CircuitVal(0, 0), 
                max_val=CircuitVal(0.7, 0.6), 
                port_type=PortType.SINK)

cpu_footprint2 = {}
cpu_footprint2[cpu_power2.name] = cpu_power2
cpu_footprint2[cpu_gnd2.name] = cpu_gnd2

cheap_cpu = Part(name="cheap_cpu",
                    cost=5,
                    footprint=cpu_footprint,
                    part_type=PartType.MICROCONTROLLER)
                    
middle_cpu = Part(name="middle_cpu",
                    cost=15,
                    footprint=cpu_footprint2,
                    part_type=PartType.MICROCONTROLLER)
                    
expensive_cpu = Part(name="expensive_cpu",
                    cost=40,
                    footprint=cpu_footprint,
                    part_type=PartType.MICROCONTROLLER)

cpus = [cheap_cpu, middle_cpu, expensive_cpu]
                     


    