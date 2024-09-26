// Based on Tim Mattson's code for
// https://github.com/tgmattso/OpenMP_intro_tutorial
#include <stdio.h>
#include <time.h>

int main() {
  unsigned int num_steps = 100000000;
  double step = 1.0 / num_steps;

  clock_t start = clock();

  double sum = 0;

  for (unsigned int i = 0; i < num_steps; i++) {
    double x = (i + 0.5) * step;
    sum += 4.0 / (1.0 + x * x);
  }

  double pi = step * sum;
  clock_t end = clock();

  printf("pi is %f in %fs!\n", pi, ((double)(end - start)) / CLOCKS_PER_SEC);

  return 0;
}
