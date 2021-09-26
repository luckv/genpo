import random

import random_generators as gens


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
    int_low, int_up = gens.easy_num_interval(min_choices=n)

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
