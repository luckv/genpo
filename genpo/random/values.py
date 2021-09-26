
import random
from fractions import Fraction
from math import ceil


def rand_bool():
    """Random bool value"""
    return bool(random.getrandbits(1))


def easy_num_interval(negative: bool = True, min_choices: int = None):
    """
    Generate an interval of integer containing at least min_choices elements. The elements contains at least 7 elements
    If negative is false the interval contains only values >= 0

    returns: tuple[int] - A tuple of two elements representing the interval generated. The first is the lower bound, the second the upper bound.
    """

    min_choices = 7 if min_choices == None else max(7, abs(min_choices))

    upper_bound = min_choices - 1
    if negative:
        upper_bound = upper_bound/2

    upper_bound = ceil(upper_bound)

    return (-upper_bound, upper_bound) if negative else (0, upper_bound)


def rand_easy_num(negative: bool = True, min_choices: int = None):
    """
    Random easy number. See 'easy_num_interval()'
    """

    low, up = easy_num_interval(negative, min_choices)
    return random.randint(low, up)


fractions = [Fraction(1, 3), Fraction(1, 2), Fraction(1, 4)]

def rand_simple_fraction():
    """
    Random simple fraction\n
    A simple fraction is one of these: 1/3, 1/2, 1/4
    """
    return random.choice(fractions)

def rand_span(values: list, target_length: int):
    """
    Span the values in the list to generate a longer list picking random values from the original list\n

    parameters: 
        - values: list - List of values
        - target_length: int  - Length of the generated list

    returns: list - A list of length specified
    raise: ValueError if target_length is not at least as the length of the list passed
    """

    unique_values_len = len(values)

    if target_length < unique_values_len:
        raise ValueError(
            f"target length ({target_length}) can't be less than unique_values array (len {values.__len__()})")

    if unique_values_len == target_length:
        return values

    return values + [random.choice(values) for _ in range(target_length - unique_values_len)]

def rand_high_coff():
    """
    Generate the highest coefficient of the polinomy.\n
    It's a random number with these probabilities:
     - 25% is -1
     - 25% is 1
     - 25% is the negative value of `rand_simple_fraction()`
     - 25% is the positive value of `rand_simple_fraction()`
    """

    sign = 1 if rand_bool() else -1
    abs_val = 1 if rand_bool() else rand_simple_fraction()

    return sign * abs_val
