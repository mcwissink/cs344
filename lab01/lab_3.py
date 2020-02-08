
"""
The One Way Door Problem.

In order to achieve the goal, the agent has to be outside the one way door with the apple.
The agent cannot re-enter the room after leaving. Since the GPS evaluates the goals in the
order given, it can easily get stuck in a state without irreversible operations.

@author: Mark Wissink 
"""

from gps import gps
import logging

logging.basicConfig(level=logging.DEBUG)

# Formulate the problem states and actions.
problem = {

    'initial': ['at door', 'in room'],
    'goal': ['out of room', 'has apple'],
    'goal_reordered': ['has apple', 'out of room'],
    'actions': [
        {
            'action': 'walk left and grap apple',
            'preconds': ['in room', 'at door'],
            'add': ['left of door', 'has apple'],
            'delete': ['at door' ]
        },
        {
            'action': 'walk right',
            'preconds': ['in room', 'left of door'],
            'add': ['at door'],
            'delete': ['left of door']
        },
        {
            'action': 'leave room',
            'preconds': ['at door', 'in room'],
            'add': ['out of room'],
            'delete': ['at door', 'in room']
        },
    ]
}

if __name__ == '__main__':

    # Failed example of the plan.
    # The GPS first tries to achieve 'out of room'
    # but then it can't renter and grab the apple
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
    # The apple is grabbed first before leaving
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
