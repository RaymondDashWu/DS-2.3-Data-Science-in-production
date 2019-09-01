import argparse

def summation(x, y):
    parser = argparse.ArgumentParser(description = 'Sum n integers.')

    parser.add_argument('integers', type = int, nargs = '+')
    parser.add_argument(dest = 'accumulate', action = 'store_const', const = sum, default = max)

    args = parser.parse_args()
    return args
    # return args.accumulate(args.integers)

print(summation(1, 2))