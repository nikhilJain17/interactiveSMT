from ismt import *
from part_library import *
from optimization import *

# Just wire a CPU's power and ground to a PSU
parts = [cheap_cpu, expensive_psu]
pwr_conn = Connection(cid=0, left_port=cheap_cpu.footprint["cpu_power"], right_port=expensive_psu.footprint["psu_positive"])
gnd_conn = Connection(cid=1, left_port=cheap_cpu.footprint["cpu_ground"], right_port=expensive_psu.footprint["psu_negative"])
connections = [pwr_conn, gnd_conn]

ckt = Circuit(parts=parts, connections=connections)
print(ckt)
simulated_annealing(start_state=ckt, num_iterations=5)