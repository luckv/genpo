
import measure
from genpo import pol_operations as ops

pol1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pol2 = [11, 12, 13, 14]
min_print_grade = (len(pol1) - 1)*2 + (len(pol2) - 1)*2

def before_benchmark():
    print(f"pol1 = {ops.coff_str(pol1)}")
    print(f"pol2 = {ops.coff_str(pol2)}")

def benchmark_sum():
    before_benchmark()

    sum_of_pols = ops.sum_pols(pol1, pol2)
    measure.measure_executions(lambda: ops.sum_pols(pol1, pol2), n=100000,
                            desc=f"pol1 + pol2 = {ops.coff_str_monotone(sum_of_pols, min_print_grade)}", show_progress=False)

    sum_of_pols = ops.sum_pols(pol1, pol2, pol1, pol2)
    measure.measure_executions(lambda: ops.sum_pols(pol1, pol2, pol1, pol2), n=100000,
                            desc=f"sum pol1 + pol2 + pol1 + pol2 = {ops.coff_str_monotone(sum_of_pols, min_print_grade)}", show_progress=False)

def benchmark_product():
    before_benchmark()

    product_of_pols = ops.multiply_pols(pol1, pol2)
    measure.measure_executions(lambda: ops.multiply_pols(pol1, pol2), n=100000,
                            desc=f"pol1*pol2 = {ops.coff_str_monotone(product_of_pols, min_print_grade)}", show_progress=False)

    product_of_pols = ops.multiply_pols(pol1, pol2, pol2, pol1)
    measure.measure_executions(lambda: ops.multiply_pols(pol1, pol2, pol2, pol1), n=100000,
                            desc=f"pol1*pol2*pol2*pol1 = {ops.coff_str_monotone(product_of_pols, min_print_grade)}", show_progress=False)