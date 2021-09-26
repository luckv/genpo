"""
    Random generators for polynomials, with or without roots

    fz functions
    -----
    The 'fz' prepended in a function name, means that the polinomy generated has the sum of multeplicities of all its roots equal to its degree.
"""

import random
from math import ceil, floor

import genpo.operations as ops
import genpo.polynomials as pols
import genpo.random.roots as roots
import genpo.random.values as gens


def fz_from_multiplicities(zeroes_multiplicity: list[int], highest_coff=None):
    """
    Generate a polinomy with integer zeroes that are easy to solve. The sum of multeplicities of all the zeroes passed is the grade of the polinomy.

    parameter: list[int] - List of zeroes of the polinomy. Each zero is repeated in the list many times as its multeplicity

    returns: list - List of coefficients of the polinomy. The element at the index i is the cofficient of x^i.
    """

    if len(zeroes_multiplicity) < 1:
        raise ValueError(
            "length of zeroes_multiplicity must be at least one. This function can't generate a polinomy without zeroes")

    roots.raise_if_not_valid_multiplicities(multiplicities=zeroes_multiplicity)

    coff = pols.from_roots(zeroes_multiplicity)

    ops.apply_factor(coff, highest_coff if highest_coff !=
                 None else gens.rand_high_coff())
    return coff

def genpo_fz_multiplicities(multiplicities: list[int], show_zeroes=False):

    zeroes_multiplicity = roots.generate_zeroes_with_multiplicity(
        multiplicities)

    coff = fz_from_multiplicities(zeroes_multiplicity)

    if show_zeroes:
        zeroes_multiplicity.sort()
        print(f'Zeroes with multiplicity: {zeroes_multiplicity}')

def genpo_fz_count(grade: int, zeroes_count: int = None, show_zeroes=False):
    """
    Generate a polinomy with integer zeroes that are easy to solve. The sum of multeplicities of all zeroes of this polinomy is its grade

    parameters:
     - grade: int - Grade of the polinomy. Can't be less than the number of zeroes
     - zeroes_count: int - Number of zeroes of the polinomy. They will be all zeroes easy to find. If no value is passed or the value `None` is passed, a polinomy with the number of zeroes equal its grade will be generated. For more information see `generate_zeroes(int)`
     - show_zeroes: bool - True to print the zeroes of the generated polinomy to stdout

     returns: list - List of coefficients of the polinomy. The element at the index i is the cofficient of x^i.
    """

    if zeroes_count == None:
        zeroes_count = grade

    if grade < zeroes_count:
        raise ValueError(
            f"polinomy grade ({grade}) can't be less than zeros_count ({zeroes_count})")

    if zeroes_count < 1:
        raise ValueError(
            "zeroes_count can't be <= 0. There must be at least one zero")

    zeroes = roots.generate_zeroes(zeroes_count)
    zeroes_multiplicity = gens.rand_span(zeroes, grade)

    coff = fz_from_multiplicities(zeroes_multiplicity)

    if show_zeroes:
        zeroes_multiplicity.sort()
        print(f'Zeroes with multiplicity: {zeroes_multiplicity}')

    return coff

def genpo_parabola_no_zeroes():
    """
    Generate a second grade polinomy without zeroes. The cofficients of this polinomy are all integer numbers, and a is 1

    return: list - List of coefficients of polinomy of the form x^2 + bx + c. The element at the index i is the cofficient of x^i.
    """
    c = gens.rand_easy_num(negative=False) + 1
    # Get a random value of b in a way that the calculated delta is negative
    max_abs_b_value = 2 * floor(sqrt(c)) - 1
    b = 0 if max_abs_b_value <= 0 else random.randint(
        -1 * max_abs_b_value, max_abs_b_value)

    return pols.parabola(1, b, c)

def genpo_1(multiplicities: list[int] = None, grade: int = None, show_zeroes=False):
    """
    Generate a polinomy with integer zeroes that are easy to solve. The grade of this polinomy is at least the sum of the multeplicities passed.

    parameters:
     - grade: int - Optional. Grade of the polinomy.
     - multiplicities: list[int] - Optional. Number of multiplicities of single zeroes in the polinomy. They will be all zeroes easy to find. 
        If no value is passed or the value `None` is passed, a polinomy with the number of zeroes equal the passed grade will be generated. For more information see `generate_zeroes(int)`
     - show_zeroes: bool - `True` to print the zeroes of the generated polinomy to stdout

     returns: list - List of coefficients of the polinomy. The element at the index i is the cofficient of x^i.
    """

    if grade == None and multiplicities == None:
        raise ValueError(
            "Must pass at least grade or multiplicities of zeroes of the polinomy to generate")

    if multiplicities == None:
        multiplicities = [1] * grade

    if grade == None:
        grade = sum(multiplicities)

    roots.raise_if_not_valid_multiplicities(
        multiplicities, sum_max=grade, sum_min=None)

    sum_multeplicities = sum(multiplicities)
    grade_without_zeroes = grade - sum_multeplicities

    if grade_without_zeroes > 0 and grade_without_zeroes % 2 != 0:
        raise ValueError(
            f"Can't generate polinomy that has grade {grade} and sum of multeplicities {sum_multeplicities}: Can't generate a polinomy without zeroes of grade {grade_without_zeroes}")

    zeroes_with_multiplicity = roots.generate_zeroes_with_multiplicity(
        multiplicities)
    coff_with_zeroes = fz_from_multiplicities(
        zeroes_with_multiplicity, highest_coff=1)

    # Generate 2nd grade polinomies without zeroes to increment the grade of the polinomy without adding zeroes
    coffs_without_zeroes = [prbs.genpo_2nd_grade_no_zeroes()
                            for _ in range(int(grade_without_zeroes / 2))]

    res = ops.multiply(coff_with_zeroes, *coffs_without_zeroes)

    # Generate the highest coefficient
    highest_coff = gens.rand_high_coff()
    ops.apply_factor(res, highest_coff)

    if show_zeroes:
        zeroes_with_multiplicity.sort()
        print(f'Zeroes with multiplicity: {zeroes_with_multiplicity}')

    return res


def genpo_2(min_grade: int = None, max_grade: int = None, min_zeroes: int = None, max_zeroes: int = None, min_multeplicity: int = None, max_multeplicity: int = None):

    if min_grade == None or min_grade < 2:
        min_grade = 2

    if max_grade == None:
        max_grade = min_grade + 3

    if max_grade < min_grade:
        raise ValueError(
            f"Interval for polynomy grade is invalid: max_grade({max_grade}) <  min_grade({min_grade})")

    if min_zeroes == None or min_zeroes < 0:
        min_zeroes = 0

    if max_zeroes != None and max_zeroes < min_zeroes:
        raise ValueError(
            f"Interval for number of zeroes is invalid: max_zeroes({max_zeroes}) < min_zeroes({min_zeroes})")

    if max_grade < min_zeroes:
        raise ValueError(
            f"Can't generate a polinomy with a max_grade of {max_grade} and min_zeroes of {min_zeroes}: values not compatible")

    if max_zeroes == None or max_zeroes > max_grade:
        max_zeroes = max_grade

    min_grade = max(min_grade, min_zeroes)

    if min_multeplicity != None and max_multeplicity != None:
        if max_multeplicity < min_multeplicity:
            raise ValueError(
                f"Can't generate zeroes with a min_multeplity of {min_multeplicity} and max_multeplicity of {max_multeplicity}: values not compatible")
    else:
        if min_multeplicity == None:
            min_multeplicity = max(1, 0 if max_zeroes == 0 else floor(
                min_grade / max_zeroes))

        if max_multeplicity == None:
            max_multeplicity = max(min_multeplicity, 0 if min_zeroes == 0 else ceil(
                max_grade / min_zeroes))

    zeroes_count = random.randint(min_zeroes, max_zeroes)

    grade_with_zeroes = 0
    pol_with_zeroes = None
    if zeroes_count > 0:
        multiplicities = roots.generate_multiplicities(
            zeroes_count, min_grade, max_grade, min_multeplicity, max_multeplicity)
        zeroes = roots.generate_zeroes_with_multiplicity(multiplicities)
        pol_with_zeroes = pols.from_roots(zeroes)
        grade_with_zeroes = len(zeroes)

    grade = random.randint(max(grade_with_zeroes, min_grade), max_grade)

    if grade != grade_with_zeroes and (grade - grade_with_zeroes) % 2 != 0:
        grade -= 1

    grade_without_zeroes = grade - grade_with_zeroes
    assert grade_without_zeroes % 2 == 0

    second_grade_pols_without_zeroes = None

    if grade_without_zeroes > 0:
        second_grade_pols_without_zeroes = [
            prbs.genpo_parabola_no_zeroes() for _ in range(int(grade_without_zeroes / 2))]

    if pol_with_zeroes == None:
        if second_grade_pols_without_zeroes != None:
            return ops.multiply(*second_grade_pols_without_zeroes)
        else:
            return None

    if second_grade_pols_without_zeroes == None:
        return pol_with_zeroes

    pol = ops.multiply(pol_with_zeroes, *second_grade_pols_without_zeroes)

    ops.apply_factor(pol, gens.rand_high_coff())

    return pol
