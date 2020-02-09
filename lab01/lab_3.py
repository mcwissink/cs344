
"""
The Plane and Parachute Problem.

In order to achieve the goal, the agent has to jump out of the plane after putting on a parachute.
The agent cannot re-enter the plane after leaving. Since the GPS evaluates the goals in the
order given, it can easily get stuck in a state without irreversible operations.

@author: Mark Wissink 
"""

from gps import gps
import logging

logging.basicConfig(level=logging.DEBUG)

# Formulate the problem states and actions.
problem = {

    'initial': ['at door', 'in plane'],
    'goal': ['out of plane', 'has parachute'],
    'goal_reordered': ['has parachute', 'out of plane'],
    'actions': [
        {
            'action': 'walk left and grab parachute',
            'preconds': ['in plane', 'at door'],
            'add': ['left of door', 'has parachute'],
            'delete': ['at door' ]
        },
        {
            'action': 'walk right',
            'preconds': ['in plane', 'left of door'],
            'add': ['at door'],
            'delete': ['left of door']
        },
        {
            'action': 'leave plane',
            'preconds': ['at door', 'in plane'],
            'add': ['out of plane'],
            'delete': ['at door', 'in plane']
        },
    ]
}

if __name__ == '__main__':

    # Failed example of the plan.
    # The GPS first tries to achieve 'out of plane'
    # but then it can't renter and grab the parachute
    #
    # A human could easily see how to solve the problem however
    actionSequenceFail = gps(
        problem['initial'],
        problem['goal'],
        problem['actions']
    )

    # Print the solution, if there is one.
    if actionSequenceFail is not None:
        for action in actionSequenceFail:
            print(action)
    else:
        print('plan failure...')

    # The succesful implementation where the goals are reordered
    # The parachute is grabbed first before leaving
    actionSequence = gps(
        problem['initial'],
        problem['goal_reordered'],
        problem['actions']
    )

    # Print the solution, if there is one.
    if actionSequence is not None:
        for action in actionSequence:
            print(action)
    else:
        print('plan failure...')
