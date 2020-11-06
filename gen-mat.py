import argparse

from Matrix import Matrix, MatrixWriter

parser = argparse.ArgumentParser(description="Create 2D arrays of random integers")
parser.add_argument("--rows", "-r", type=int, required=True, help="Rows in matrix")
parser.add_argument("--cols", "-c", type=int, required=True, help="Columns in matrix")
parser.add_argument("--min", type=int, default=1, help="Minimum value")
parser.add_argument("--max", type=int, default=100, help="Maximum value")
parser.add_argument("filename")
args = parser.parse_args()

if args.min > args.max:
    raise RuntimeError(f"Bogus range of values [{args.min}..{args.max}]")

m = Matrix.from_random(args.rows, args.cols, args.min, args.max)
mw = MatrixWriter(args.rows, args.cols, args.filename)
mw.write_matrix(m, close=True)
