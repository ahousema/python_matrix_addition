import argparse

from Matrix import Matrix, MatrixReader, MatrixWriter
from MultiTimer import MultiTimer
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
num_procs = comm.Get_size()

dimensions = []
rows_per_proc = 1

parser = argparse.ArgumentParser(description="Add 2D arrays of integers")
parser.add_argument("a")
parser.add_argument("b")
parser.add_argument("c")
args = parser.parse_args()

mt = MultiTimer()

# Calculate the sizes of things
if rank == 0:
    mt.record("Calculate Sizes")
    dimensions = MatrixReader(args.a).read_dimensions()
    print(dimensions[0])

    rows_per_proc = int(dimensions[0])/num_procs

# Distribute and recieve work
if rank == 0:
    mt.record("Read/Send Work")
    a = MatrixReader(args.a).read_matrix(num_rows=rows_per_proc, close=False)
    b = MatrixReader(args.b).read_matrix(num_rows=rows_per_proc, close=False)
    for to_proc in range(1, num_procs):
        comm.send(a, dest=to_proc, tag=1)
        comm.send(b, dest=to_proc, tag=1)
        if to_proc != num_procs - 1:
            a = MatrixReader(args.a).read_matrix(
                num_rows=rows_per_proc, close=False)
            b = MatrixReader(args.b).read_matrix(
                num_rows=rows_per_proc, close=False)
    a = MatrixReader(args.a).read_matrix(num_rows=rows_per_proc, close=True)
    b = MatrixReader(args.b).read_matrix(num_rows=rows_per_proc, close=True)
else:
    a = comm.recv(source=0, tag=1)
    b = comm.recv(source=0, tag=1)

# Do addition
# ***** The flags parameter adds some starts to make this one easy to find.
mt.record("Add", flags=2)
c = a + b

# Send result back to rank 0 and then write matrix
if rank == 0:
    mt.record("Write")
    c_temp = c
    for from_proc in range(1, num_procs):
        c = comm.recv(source=from_proc, tag=1)
        MatrixWriter(c.rows, c.cols, args.c).write_matrix(c, close=False)
    c = c_temp
    MatrixWriter(c.rows, c.cols, args.c).write_matrix(c, close=True)
else:
    mt.record("Send")
    comm.send(c, dest=0, tag=1)

# ***** The MultiTimer class automatically adds a STOP entry.
# mt.record("Complete")
mt.report(f"{rank} ")
