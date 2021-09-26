
import random

import genpo.random.polynomials as genpo
import genpo.representation as repr


def main_full_zeroes(pols: int = 1):
    for _ in range(pols):
        # Create a polinomy with 2 or 3 zeroes and maxinum one zero with multiplicity 2
        zeroes_count = random.randint(2, 3)
        pol_grade = random.randint(3, zeroes_count + 1)

        coff = genpo.genpo_fz_count(pol_grade, zeroes_count=zeroes_count)

        print(f'Coefficients: {repr.coff_str(coff)}')
