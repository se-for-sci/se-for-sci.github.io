#include <stdio.h>
#include <stdlib.h>

#define N 512

// kernel: each block adds one element
__global__ void add(int *a, int *b, int *c) {
  c[blockIdx.x] = a[blockIdx.x] + b[blockIdx.x];
}

void random_ints(int *x, int size) {
  int i;
  for (i = 0; i < size; i++) x[i] = rand() % 10;
}

int main(void) {
  int *a, *b, *c;        // host copies of a, b, c
  int *a_d, *b_d, *c_d;  // device copies of a, b, c
  int size = N * sizeof(int);
  int i, errors = 0;

  // Alloc space for device copies of a, b, c
  cudaMalloc((void **)&a_d, size);
  cudaMalloc((void **)&b_d, size);
  cudaMalloc((void **)&c_d, size);

  // Alloc space for host copies of a, b, c and setup input values
  a = (int *)malloc(size); random_ints(a, N);
  b = (int *)malloc(size); random_ints(b, N);
  c = (int *)malloc(size);

  // Copy inputs to device
  cudaMemcpy(a_d, a, size, cudaMemcpyHostToDevice);
  cudaMemcpy(b_d, b, size, cudaMemcpyHostToDevice);

  // Launch add() kernel on GPU with N blocks of 1 thread
  add<<<N, 1>>>(a_d, b_d, c_d);

  // Copy result back to host
  cudaMemcpy(c, c_d, size, cudaMemcpyDeviceToHost);

  // Check the result on the host
  for (i = 0; i < N; i++)
    if (c[i] != a[i] + b[i]) errors++;
  printf("%d errors\n", errors);

  // Check for errors (from the API calls or from the kernel)
  printf("%s\n", cudaGetErrorString(cudaGetLastError()));

  // Cleanup
  free(a); free(b); free(c);
  cudaFree(a_d); cudaFree(b_d); cudaFree(c_d);
  return 0;
}
