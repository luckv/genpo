"""String representations of polynomials"""
from functools import reduce

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
