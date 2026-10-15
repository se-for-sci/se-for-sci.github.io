// Based on Tim Mattson's code for
// https://github.com/tgmattso/OpenMP_intro_tutorial
#include <mpi.h>
#include <stdio.h>

int main(int argc, char **argv) {
  unsigned int num_steps = 100000000;
  double step = 1.0 / num_steps;

  MPI_Init(&argc, &argv);

  int my_id, num_procs;
  MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
  MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
  printf("Hello from %i of %i\n", my_id, num_procs);

  MPI_Barrier(MPI_COMM_WORLD);
  double start = MPI_Wtime();

  double sum = 0;

  unsigned int imin = (unsigned long long)my_id * num_steps / num_procs;
  unsigned int imax = (unsigned long long)(my_id + 1) * num_steps / num_procs;

  for (unsigned int i = imin; i < imax; i++) {
    double x = (i + 0.5) * step;
    sum += 4.0 / (1.0 + x * x);
  }

  double sum_total;
  MPI_Reduce(&sum, &sum_total, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

  if (my_id == 0) {
    double pi = step * sum_total;
    double end = MPI_Wtime();

    printf("pi is %f in %fs!\n", pi, end - start);
  }

  MPI_Finalize();

  return 0;
}
