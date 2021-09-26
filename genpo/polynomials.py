"""Functions to create polynomials from parameters"""

def parabola(a=1, b=1, c=1):
    """
    Generate a second degree polinomy, with the parameters specified.

    Returns: 
        list - List of coefficients of polinomy of the form ax^2 + bx + c
    """
    return [c, b, a]

def from_roots(zeroes: list):

    """
    Generate the coefficients of a polinomy that has the roots specified in the list. The multeplicity of each root is determined by how many times it appears in the list.

    Parameter: 
        list - List of roots. If a root has a multiplicity of m, it will appear m times in the list. Btw, the length of list is the degree of the polinomy.

    Returns:
        list: Coefficients of the polinomy. The element at the index i is the cofficient of x^i.
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