"""Functions for manipulating roots and multiplicities"""

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
