
import random
from fractions import Fraction
from math import ceil, floor, sqrt

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


def generate_zeroes(n: int):
    """
    Generate `n` random distinct zeroes, all simple to find when resolving a polinomy\n

    parameter: int - The number of zeroes to generate. It's a value greater of 0
    returns: list(int) - The generated zeroes
    raise: ValueError if `n` is < 0
    """

    if n < 0:
        raise ValueError("n can't be negative")

    zeroes: set[int] = set()

    # Generate a random zero choosing from an interval
    int_low, int_up = easy_num_interval(min_choices=n)

    while len(zeroes) < n:
        zeroes = zeroes | {random.randint(int_low, int_up)
                           for _ in range(n - len(zeroes))}

    return list(zeroes)


def keep_valid_multiplicities(mul: list[int]):
    """
    Filter the elements of the list are >= 1
    """
    return [v for v in mul if v >= 1]


def raise_if_not_valid_multiplicities(multiplicities: list[int], sum_max=None, sum_min=1):
    """
    Raise a ValueError if one of this conditions are met:
        - the multiplicities parameter contains a value <= 0
        - if sum_max is not None and the sum of all values in the list is > of sum_max
        - if sum_min is not None and the sum of all values in the list is < sum_min
    """

    if sum_max != None and sum_min != None and sum_max < sum_min:
        raise ValueError("max can't be less than min")

    if any(v <= 0 for v in multiplicities):
        raise ValueError(
            "Can't have a multiplicity of a zero that is less than 0")

    if sum_max != None or sum_min != None:
        full_zeroes_grade = sum(multiplicities)

        if sum_max != None and full_zeroes_grade > sum_max:
            raise ValueError(
                f"The sum of all multeplicities({full_zeroes_grade}) can't be greater than max({sum_max})")

        if sum_min != None and full_zeroes_grade < sum_min:
            raise ValueError(
                f"The sum of all multeplicities({full_zeroes_grade}) can't be less than min({sum_min})")


def generate_multiplicities(zeroes: int = 1, min_grade: int = None, max_grade: int = None, min_multiplicity: int = None, max_multiplicity: int = None):
    """
    Generate random multiplicities for a polinomy, using the constraints specified.

    parameters:
        zeroes: int - Number of zeroes to generate. An integer >= 1
        min_grade, max_grade: int - If one of the values or both are specified, the grade of the polinomy with these zeroes will be in the range specified by the values
        min_multiplicity, max_multiplicity: int - Must pass both values or no one. If not specified each zero will have multeplicity 1. min_multeplicitiy will be constrained to have minimum value of 1 and max_multiplicity to the have the minimum value of min_multiplicity
    """

    if zeroes == None or zeroes < 1:
        raise ValueError(f"Can't generate {zeroes} zeroes")

    if min_grade != None and max_grade != None and max_grade < min_grade:
        raise ValueError(
            f"Can't have min_grade={min_grade} and max_grade={max_grade}: values incompatible")

    if (min_multiplicity == None) != (max_multiplicity == None):
        raise ValueError(
            "Must pass both min_multiplicty and max_multiplicity params, or no one of the two")

    if min_multiplicity != None and max_multiplicity != None:
        if max_multiplicity < min_multiplicity:
            raise ValueError(
                f"Can't have min_multiplicity={min_multiplicity} and max_multiplicity={max_multiplicity}: values incompatible")
        else:
            # Constrain the interval of multeplicity
            if min_multiplicity < 1:
                min_multiplicity = 1

            if max_multiplicity < min_multiplicity:
                max_multiplicity = min_multiplicity
    else:
        min_multiplicity = max_multiplicity = 1

    multiplicities = [random.randint(
        min_multiplicity, max_multiplicity) for _ in range(zeroes)]

    if min_grade == None and max_grade == None:
        return multiplicities

    total_sum = sum(multiplicities)

    # Constrain the grade of the polinomy in the interval passed, if necessary
    if max_grade != None and total_sum > max_grade:
        diff = total_sum - max_grade
        i = 0
        while diff > 0 and i < zeroes:
            if multiplicities[i] > min_multiplicity:
                i_diff = min(multiplicities[i] - min_multiplicity, diff)
                diff -= i_diff
                multiplicities[i] = multiplicities[i] - i_diff
            i += 1
    else:
        if min_grade != None and total_sum < min_grade:
            diff = min_grade - total_sum
            i = 0
            while diff > 0 and i < zeroes:
                if multiplicities[i] < max_multiplicity:
                    i_diff = min(max_multiplicity - multiplicities[i], diff)
                    diff -= i_diff
                    multiplicities[i] = multiplicities[i] + i_diff
                i += 1

    return multiplicities


def generate_zeroes_with_multiplicity(multiplicities: list[int]):
    """
    Generate a list with random zeroes, all simple to find when resolving a polinomy. All values are repeated as many times as their multiplicity indicated a value of the desc list

    parameter: list[int] - A list of values >= 1. Every item in the set represents a zero, and its value the zero's multiplicity

    returns: list[int] - A list of zeroes. Every zero is repeated in the list as many times as its multiplicity.
    """

    with_multiplicity = keep_valid_multiplicities(multiplicities)
    raise_if_not_valid_multiplicities(multiplicities)

    # Generate the zeroes and repete each one as many times as its multiplicity
    zeroes = []
    for zero, mul in zip(generate_zeroes(len(with_multiplicity)), with_multiplicity):
        zeroes = zeroes + [zero] * mul

    return zeroes


def span_random(values: list, target_length: int):
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


def generate_coefficients(zeroes: list):
    """
    Generate the coefficients of a polinomy that has the zeroes specified in the list. Every zero in the list passed has to appear as many times as its multiplicity.

    parameter: list - List of zeroes. If a zero has a multiplicity of m, will appear m times in the list. Btw, the length of list + 1 is the grade of the polinomy.
    return: list - List of coefficients of the polinomy. The element at the index i is the cofficient of x^i.
    """

    n = len(zeroes) + 1
    coff = [1 for _ in range(n)]

    # The iteration i does a multiplication between the partial polinomy built and (x - zeroes[i])
    for i in range(n - 1):

        # Sum the partial array shifted of one position to the end with the array multiplied with -zeroes[i]
        # In this way we emulate the addition of the polinomies created with the product of x and -zeroes[i]
        zero = zeroes[i]
        t0 = 0
        for j in range(i+1):
            t1 = t0
            t0 = coff[j]
            coff[j] = t1 - (t0 * zero)

    return coff


def generate_high_coff():
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


def pol_2nd_grade(a=1, b=1, c=1):
    """
    Generate a second grade polinomy, with the parameters specified.

    return: list - List of coefficients of polinomy of the form ax^2 + bx + c
    """
    return [c, b, a]


def genpo_2nd_grade_no_zeroes():
    """
    Generate a second grade polinomy without zeroes. The cofficients of this polinomy are all integer numbers, and a is 1

    return: list - List of coefficients of polinomy of the form x^2 + bx + c. The element at the index i is the cofficient of x^i.
    """
    c = rand_easy_num(negative=False) + 1
    # Get a random value of b in a way that the calculated delta is negative
    max_abs_b_value = 2 * floor(sqrt(c)) - 1
    b = 0 if max_abs_b_value <= 0 else random.randint(
        -1 * max_abs_b_value, max_abs_b_value)

    return pol_2nd_grade(1, b, c)
