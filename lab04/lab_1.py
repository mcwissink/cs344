"""
Lab 4

@author: Mark Wissink (mcw33)
@version Feb 28, 2020
"""
from probability import JointProbDist, enumerate_joint_ask

"""
Exercise 4.1

1. P(Cavity | Catch=True) = (0.108 + 0.072) / (0.108 + 0.072 + 0.016 + 0.144) = 0.529

"""
"""
2.
"""
# The Joint Probability Distribution Fig. 13.3 (from AIMA Python)
P = JointProbDist(['Toothache', 'Cavity', 'Catch'])
T, F = True, False
P[T, T, T] = 0.108; P[T, T, F] = 0.012
P[F, T, T] = 0.072; P[F, T, F] = 0.008
P[T, F, T] = 0.016; P[T, F, F] = 0.064
P[F, F, T] = 0.144; P[F, F, F] = 0.576

# Compute P(Cavity|Catch=T) 
PC = enumerate_joint_ask('Cavity', {'Catch': T}, P)
print(PC.show_approx())

"""
P(Coin1 | Coin2=Heads) = 0.25 / (0.25 + 0.25) = 0.5
3. 
"""
P = JointProbDist(['Coin1', 'Coin2'])
H, T = 'Heads', 'Tails'
P[H, H] = 0.25; P[T, T] = 0.25
P[T, H] = 0.25; P[H, T] = 0.25

PC = enumerate_joint_ask('Coin2', {'Coin1': T}, P)
print(PC.show_approx())
