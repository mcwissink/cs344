"""
This module implements local search on a simple abs function variant.
The function is a linear function  with a single, discontinuous max value
(see the abs function variant in graphs.py).

@author: kvlinden
@author: mcw33
@version 6feb2013
"""
from search import Problem, hill_climbing, simulated_annealing, \
    exp_schedule, genetic_search
from random import randrange
import math

class SineVariant(Problem):
    """
    State: x value for the abs function variant f(x)
    Move: a new x value delta steps from the current x (in both directions) 
    """
    
    def __init__(self, initial, delta=0.001):
        self.initial = initial
        self.delta = delta
        
    def actions(self, state):
        return [state + self.delta, state - self.delta]
    
    def result(self, stateIgnored, x):
        return x
    
    def value(self, x):
        return math.fabs(x * math.sin(x)) 


if __name__ == '__main__':
    hill_solution_max = 0
    annealing_solution_max = 0
    hill_total = 0
    annealing_total = 0
    
    restarts = 100
    maximum = 30
    for iteration in range(0, restarts): 
        # Formulate a problem with a 2D hill function and a single maximum value.
        initial = randrange(0, maximum)
        p = SineVariant(initial, delta=2)

        # Solve the problem using hill-climbing.
        hill_solution = hill_climbing(p)
        hill_total += p.value(hill_solution)
        # Check if we found a better hill-climbing solution.
        if p.value(hill_solution) > p.value(hill_solution_max):
            hill_solution_max = hill_solution

        # Solve the problem using simulated annealing.
        annealing_solution = simulated_annealing(
            p,
            exp_schedule(k=20, lam=0.005, limit=1000)
        )
        annealing_total += p.value(annealing_solution)
        # Check if we found a better simulated annealing solution.
        if p.value(annealing_solution) > p.value(annealing_solution_max):
            annealing_solution_max = annealing_solution

        
    print('Initial                      x: ' + str(p.initial)
          + '\t\tvalue: ' + str(p.value(initial))
    )
    print('Hill-climbing solution       x: ' + str(hill_solution_max)
          + '\tvalue: ' + str(p.value(hill_solution_max))
    )
    print('Simulated annealing solution x: ' + str(annealing_solution_max)
          + '\tvalue: ' + str(p.value(annealing_solution_max))
    )
    print('Hill-climbing average: ' + str(hill_total/restarts))
    print('Simluated anneainlg averge: ' + str(annealing_total/restarts))
