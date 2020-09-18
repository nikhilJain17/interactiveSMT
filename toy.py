from z3 import *
import random


################################################
## Simulated Annealing 

# energy function E(state) :: Int
#   - fitness function 
#   - (lower is better)

# acceptance probability function P(e, e_new, temp)
#   - probability of choosing new state 

# annealing schedule --> how you pick neighbors

# Let s = s0 (initial state)
# For k = 0 through kmax (exclusive): (number of steps)
    # T ← temperature( (k+1)/kmax )
    # Pick a random neighbour, snew ← neighbour(s)
    # If P(E(s), E(snew), T) ≥ random(0, 1): 
        # s ← snew
# Output: the final state s

# Prob(accepting uphill move) ~ 1 - exp(deltaE / kT))
################################################

# fitness function -> canonically, lower fitness is better
def energy_function(state):
    # check sat with solver
    s2 = Solver()
    a, b, c, d = state[0], state[1], state[2], state[3]
    s2.add((a + b + c + d == 100))
    # s2.add(((a - b + c - d) > 1))

    # wrong solutions are weighted by how far off they are
    if s2.check() == unsat:
        return abs(100 - (a + b + c + d))

    # correct solutions are always better than wrong solutions
    return -1 * abs(state[0])

# get a neighbor from the current state
def get_neighbor(state, temperature):
    # twiddle state a bit to randomly get a neighbor
    new0 = state[0] + (random.randint(-10,10) * temperature)
    new1 = state[1] + (random.randint(-10,10) * temperature)
    new2 = state[2] + (random.randint(-10,10) * temperature)
    new3 = state[3] + (random.randint(-10,10) * temperature)

    return (int(new0), int(new1), int(new2), int(new3))

def simulated_annealing(start_state, num_iterations):
    # annealing log
    # states_used = []
    # costs = []

    curr_soln = start_state # (a, b, c, d)
    curr_cost = energy_function(curr_soln)

    for i in range(1, num_iterations + 1):
        temperature = i / num_iterations

        new_state = get_neighbor(start_state, temperature)
        new_cost = energy_function(new_state)

        # always accept a better state
        # otherwise randomly accept or reject state
        if new_cost < curr_cost:
            curr_soln = new_state
            curr_cost = new_cost
        else:
            p = math.exp(- (new_cost - curr_cost) / temperature)
            if p > random.random():
                curr_soln = new_state
                curr_cost = new_cost

        print(i, curr_soln, curr_cost)
    return curr_soln, curr_cost

simulated_annealing((50,10,10,10), 2000)