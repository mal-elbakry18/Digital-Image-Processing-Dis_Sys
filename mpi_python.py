from mpi4py import MPI

def parallel_sum(n):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    chunk_size = n // size
    start = rank * chunk_size + 1
    end = (rank + 1) * chunk_size

    # If the last process, adjust end to cover all remaining numbers
    if rank == size - 1:
        end = n

    local_sum = sum(range(start, end + 1))

    # Reduce sum from all processes to get global sum
    global_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

    if rank == 0:
        print("The sum of numbers from 1 to", n, "is", global_sum)

if __name__ == "__main__":
    n = 1000000  # Change this to adjust the range of numbers to sum
    parallel_sum(n)
