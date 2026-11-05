#include <stdio.h>

// kernel: add two integers
__global__ void add(int *a, int *b, int *c) {
  *c = *a + *b;
}

int main(void) {
  int a, b, c;           // host copies of a, b, c
  int *a_d, *b_d, *c_d;  // device copies of a, b, c
  int size = sizeof(int);

  // Allocate space for device copies of a, b, c
  cudaMalloc((void **)&a_d, size);
  cudaMalloc((void **)&b_d, size);
  cudaMalloc((void **)&c_d, size);

  // Setup input values
  a = 2;
  b = 7;

  // Copy inputs to device
  cudaMemcpy(a_d, &a, size, cudaMemcpyHostToDevice);
  cudaMemcpy(b_d, &b, size, cudaMemcpyHostToDevice);

  // Launch add() kernel on GPU
  add<<<1, 1>>>(a_d, b_d, c_d);

  // Copy result back to host
  cudaMemcpy(&c, c_d, size, cudaMemcpyDeviceToHost);

  // Print the result
  printf("c = %d\n", c);

  // Check for errors (from the API calls or from the kernel)
  printf("%s\n", cudaGetErrorString(cudaGetLastError()));

  // Cleanup
  cudaFree(a_d); cudaFree(b_d); cudaFree(c_d);
  return 0;
}
