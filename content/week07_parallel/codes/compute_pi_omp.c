// Based on Tim Mattson's code for
// https://github.com/tgmattso/OpenMP_intro_tutorial
#include <stdio.h>
#include <omp.h>

int main() {
  unsigned int num_steps = 100000000;
  double step = 1.0 / num_steps;

  double start = omp_get_wtime();

  double sum = 0;

#pragma omp parallel for reduction(+ : sum)
  for (unsigned int i = 0; i < num_steps; i++) {
    double x = (i + 0.5) * step;
    sum += 4.0 / (1.0 + x * x);
  }

  double pi = step * sum;
  double end = omp_get_wtime();

  printf("pi is %f in %fs!\n", pi, end - start);

  return 0;
}
