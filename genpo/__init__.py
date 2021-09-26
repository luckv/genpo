
import random
from math import ceil, floor

import operations as ops
import parabolas as prbs
import random_generators as gens
import roots


def pol_from_zeroes(zeroes: list):
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

    coff = pol_from_zeroes(zeroes_multiplicity)

    ops.apply_factor(coff, highest_coff if highest_coff !=
                 None else gens.generate_high_coff())
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
    zeroes_multiplicity = gens.span_random(zeroes, grade)

    coff = fz_from_multiplicities(zeroes_multiplicity)

    if show_zeroes:
        zeroes_multiplicity.sort()
        print(f'Zeroes with multiplicity: {zeroes_multiplicity}')

    return coff


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

    res = ops.multiply_pols(coff_with_zeroes, *coffs_without_zeroes)

    # Generate the highest coefficient
    highest_coff = gens.generate_high_coff()
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
        pol_with_zeroes = pol_from_zeroes(zeroes)
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
            return ops.multiply_pols(*second_grade_pols_without_zeroes)
        else:
            return None

    if second_grade_pols_without_zeroes == None:
        return pol_with_zeroes

    pol = ops.multiply_pols(pol_with_zeroes, *second_grade_pols_without_zeroes)

    ops.apply_factor(pol, gens.generate_high_coff())

    return pol


def main_full_zeroes(pols: int = 1):
    for _ in range(pols):
        # Create a polinomy with 2 or 3 zeroes and maxinum one zero with multiplicity 2
        zeroes_count = random.randint(2, 3)
        pol_grade = random.randint(3, zeroes_count + 1)

        coff = genpo_fz_count(pol_grade, zeroes_count=zeroes_count)

        print(f'Coefficients: {pols.coff_str(coff)}')

if __name__ == "__main__":
    pass

