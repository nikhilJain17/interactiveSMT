from ismt import *

# Every test returns either True for sat or False for unsat
#   (1) Resolve operating limit constraints
#   (2) Ensure connections are well-defined
#       a) Both left and right port exist 
#       b) 1 port is the source and 1 port is the sink
#   (3) Possibly handle ambiguous / unassigned variables?

def print_subtest(tname: String):
    print("----------------------------------------\n")
    print(tname)
    print("----------------------------------------\n")


def test_simple_constraints() -> bool:
    TAG = \
        "===============================\ntest_simple_constraints\n===============================\n"
    print(TAG)
    print_subtest("(TEST 1) left port == right port\n")
    
    # lp == rp
    lp1:Port = Port(CircuitVal(10, 10), CircuitVal(10, 10), PortType.COPPER)
    rp1:Port = Port(CircuitVal(10, 10), CircuitVal(10, 10), PortType.COPPER)
    c1:Connection = Connection(1, lp1, rp1)
    t1:bool = design_is_sat([c1])
    
    assert(t1)
    print("\nPASSED!\n\n")

    # lp < rp
    print_subtest("(TEST 2) left port subsumed right port\n")
    # lp subsumed by rp
    lp2 = Port(CircuitVal(100, 100), CircuitVal(200, 200), PortType.COPPER)
    rp2 = Port(CircuitVal(0, 0), CircuitVal(6000, 6000), PortType.COPPER)
    c2:Connection = Connection(2, lp2, rp2)
    t2:bool = design_is_sat([c2])

    assert(t2)
    print("\nPASSED!\n\n")

    # rp subsumed by lp
    print_subtest("(TEST 3) right port subsumed left port\n")
    # lp subsumed by rp
    rp3 = Port(CircuitVal(100, 100), CircuitVal(200, 200), PortType.COPPER)
    lp3 = Port(CircuitVal(0, 0), CircuitVal(6000, 6000), PortType.COPPER)
    c3:Connection = Connection(3, lp3, rp3)
    t3:bool = design_is_sat([c3])

    print(c3)

    assert(t3)
    print("\nPASSED!\n\n")

def run_tests():
    test_simple_constraints()

def main():
    run_tests()