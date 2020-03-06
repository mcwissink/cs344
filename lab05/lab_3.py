'''
Lab 3 - Sunshine and Happiness - based off of AIMA Python code

@author: mcw33
'''

from probability import BayesNet, enumeration_ask, elimination_ask, gibbs_ask

# Utility variables
T, F = True, False

# Modelling happiness network from Exercise 5.3
happy = BayesNet([
    ('Sunny', '', 0.7),
    ('Raise', '', 0.01),
    ('Happy', 'Sunny Raise', {(T, T): 1.0, (T, F): 0.7, (F, T): 0.9, (F, F): 0.1}),
])

# a.
print(enumeration_ask('Raise', dict(Sunny=T), happy).show_approx())
print(enumeration_ask('Raise', dict(Sunny=T, Happy=T), happy).show_approx())
'''
Raise and Sunny are independent variables, so using conditional probabilities with just them alone doesn't change their probabilities.

P(Raise | Sunny) = alpha * <P(Raise) * P(Sunny), P(~Raise) * P(Sunny)>
P(Raise | Sunny) = alpha * P(Sunny) * <0.01, 0.99>
P(Raise | Sunny) = <0.01, 0.99>

With Raise given Sunny and Happy, the likelihood that the person is happy even without Raise being true is still quite high. But Raise almost guarantees happiness, so the probability that Raise is true is a little higher.

P(Raise | Happy ^ Sunny) = alpha * <P(Happy | Sunny ^ Raise) * P(Sunny) * P(Raise), P(Happy | Sunny ^ ~Raise) * P(Sunny) * P(~Raise)>
P(Raise | Happy ^ Sunny) = alpha * <1.0 * 0.7 * 0.01, 0.7 * 0.7 * 0.99>
P(Raise | Happy ^ Sunny) = <0.0142, 0.986>
'''

# b.
print(enumeration_ask('Raise', dict(Happy=T), happy).show_approx())
print(enumeration_ask('Raise', dict(Sunny=F, Happy=T), happy).show_approx())
'''
The results makes sense to me. For the first one, if happy is true, it slightly increases the chance that there was a raise since Raise does contribute to happiness, but the chances of Raise are still quite low since Happy is most likely because of Sunny. The second problem explicitly negates Sunny, so happiness can only come from a Raise, or being randomly happy when neither is true. This greatly increase the chance of Raise because it's likely to make the person happy, while there is a low chance of Happy when both Happy and Raise are false.
'''
