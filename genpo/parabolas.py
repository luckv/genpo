import random
from math import floor, sqrt

from random_generators import rand_easy_num


def parabola(a=1, b=1, c=1):
    """
    Generate a second grade polinomy, with the parameters specified.

    return: list - List of coefficients of polinomy of the form ax^2 + bx + c
    """
    return [c, b, a]


def genpo_parabola_no_zeroes():
    """
    Generate a second grade polinomy without zeroes. The cofficients of this polinomy are all integer numbers, and a is 1

    return: list - List of coefficients of polinomy of the form x^2 + bx + c. The element at the index i is the cofficient of x^i.
    """
    c = rand_easy_num(negative=False) + 1
    # Get a random value of b in a way that the calculated delta is negative
    max_abs_b_value = 2 * floor(sqrt(c)) - 1
    b = 0 if max_abs_b_value <= 0 else random.randint(
        -1 * max_abs_b_value, max_abs_b_value)

    return parabola(1, b, c)
