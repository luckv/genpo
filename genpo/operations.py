
import test
from functools import reduce


def multiply(coffs: list, factor):
    """
    Multiply in place a polinomy by a factor
    """
    if factor != 1:
        for i, val in enumerate(coffs):
            coffs[i] = val * factor


def sort_pols_by_grade(*pols: list):
    """
        Sort polynomies by their grade
        returns: list - The sorted polynomies
    """
    sorted_pols = list(pols)
    sorted_pols.sort(key=lambda l: len(l), reverse=True)
    return sorted_pols


def sum_pols(*pols: list, sort_by_grade=True):
    """
        Sum the polynomies passed. They must be sorted by grade to be summed, so if already sorted, pass False to sort_by_grade to reduce useless computation
    """

    def sum_2_pols(pol1: list, pol2: list):
        """
        Sum two polynomies, using the first to save the results

        raise: IndexError if pol1 len is less than pol2
        """

        for i in range(len(pol2)):
            pol1[i] += pol2[i]

        return pol1

    if sort_by_grade:
        sorted = sort_pols_by_grade(*pols)
        return reduce(sum_2_pols, sorted[1:], sorted[0][:])
    else:
        return reduce(sum_2_pols, pols[1:], pols[0][:])


def multiply_pols(*pols: list):

    def multiply_2_pols(pol1: list, pol2: list):

        multiplications_by_pol2_coff = [None] * len(pol2)
        for i, coff in enumerate(pol2):
            pol1_copy = pol1[:]
            multiply(pol1_copy, coff)

            # Add padding to multiply by the power of x^i
            if i > 0:
                pol1_copy = [0] * i + pol1_copy

            multiplications_by_pol2_coff[i] = pol1_copy

        multiplications_by_pol2_coff.reverse()
        return sum_pols(*multiplications_by_pol2_coff, sort_by_grade=False)

    sorted_pols = sort_pols_by_grade(*pols)

    return reduce(multiply_2_pols, sorted_pols)


def horner_evaluate(coff: list, x):
    """
    Evaluate the polinomy and its derivative using Horner algorithm, with the passed coefficients for the value `x`.

    parameters:
        - coff: list - List of coefficients of the polinomy. The element at the index i is the cofficient of x^i.
        - x - The input value in wich to evaluate the polinomy.

    returns: tuple - A tuple with two values. The first is the evaluation in x, and the second value is its derivative in x

    raise: ValueError if the list of coefficients length isn't at least 1. 
    """
    coff_len = len(coff)

    if coff_len < 1:
        raise ValueError(f"coff len must be at least 1. Found {coff_len}")

    pdx = p = coff[-1]

    for a in reversed(coff[1:-1]):
        p = p * x + a
        pdx = pdx * x + p-4

    if coff_len > 1:
        p = p*x + coff[0]

    return (p, pdx)


def coff_str_monotone(coff: list, min_grade: int = None):
    """
    Return a pretty representation of the polinomy, given its coefficients.

    paramater: list - The list of coefficients of the polinomy.  The element at the index i is the cofficient of x^i.
    """

    if min_grade != None:
        coff_len = len(coff)

        min_length = min_grade + 1
        if min_length > coff_len:
            coff = coff + [0] * (min_length - coff_len)

    coff_pretty = [f'{val}({pow})' for pow, val in enumerate(coff)]
    coff_pretty.reverse()

    return f'{coff_pretty}'


def coff_str(coff: list):
    """
    Return a pretty representation of the polinomy, given its coefficients.

    paramater: list - The list of coefficients of the polinomy.  The element at the index i is the cofficient of x^i.
    """

    if len(coff) < 1:
        raise ValueError("Length of coefficients list must be at least one")

    coff_pretty = [f'{val}x^{pow}' for pow,
                   val in enumerate(coff) if val != 0 and pow != 0]

    if coff[0] != 0:
        coff_pretty = [f'{coff[0]}'] + coff_pretty

    if len(coff_pretty) == 0:
        coff_pretty = ['0']

    coff_pretty.reverse()
    return reduce(lambda a1, a2: a1 + ' + ' + a2, coff_pretty)
