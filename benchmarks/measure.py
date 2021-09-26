import time


def measure_executions(fun, desc: str = None, n: int = 100, show_progress: bool = True):
    if desc != None:
        print("--- %s ---" % desc)

    print("--- %s executions ---" % n)

    if show_progress:
        print(" 0\t", end='')

    elasped = 0.0

    for i in range(n):
        start = time.time()
        fun()
        stop = time.time()
        elasped = elasped + (stop - start)

        if show_progress:
            if i != 0 and i % 100 == 0:
                print(f"\n {i}\t", end='')

            print(".", end='', flush=True)

    if show_progress:
        print()
    print("--- %f seconds ---" % (elasped))
    print("--- %f seconds per execution ---" % (elasped / n))
