'''
Lab 2 - Cancer - based off of AIMA Python code

@author: mcw33
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

# Modelling cancer network from Exercise 5.2
cancer = BayesNet([
    ('Cancer', '', 0.01),
    ('Test1', 'Cancer', {T: 0.9, F: 0.2}),
    ('Test2', 'Cancer', {T: 0.9, F: 0.2}),
    ])

print(enumeration_ask('Cancer', dict(Test1=T, Test2=T), cancer).show_approx())
print(enumeration_ask('Cancer', dict(Test1=T, Test2=F), cancer).show_approx())

'''
The results make sense in the context of the program. The chances of Cancer are quite small, and the false positives for the tests are quite high (20%). When both tests test true, the resulting probability of having cancer is still quite low. When one test fails, that greatly decreases the probability of having cancer.

P(Cancer | Test1 ^ Test2) = alpha * <P(Cancer) * P(Test1 | Cancer) * P(Test2 | Cancer), P(~Cancer) * P(Test1 | ~Cancer), P(Test2 | ~Cancer)>
P(Cancer | Test1 ^ Test2) = alpha * <0.01 * 0.9 * 0.9, 0.99 * 0.2 * 0.2>
P(Cancer | Test1 ^ Test2) = alpha * <0.0081, 0.0396>
P(Cancer | Test1 ^ Test2) = <0.17, 0.83>

P(Cancer | Test1 ^ ~Test2) = alpha * <P(Cancer) * P(Test1 | Cancer) * P(~Test2 | Cancer), P(~Cancer) * P(Test1 | ~Cancer), P(~Test2 | ~Cancer)>
P(Cancer | Test1 ^ ~Test2) = alpha * <0.01 * 0.9 * 0.1, 0.99 * 0.2 * 0.8>
P(Cancer | Test1 ^ ~Test2) = alpha * <0.0009, 0.1584>
P(Cancer | Test1 ^ ~Test2) = <0.00565, 0.994>
'''
