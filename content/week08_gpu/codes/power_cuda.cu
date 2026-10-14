#include <cuda.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define N 100000000
#define BLOCKSIZE 256

// parallel function: each thread computes one element of y
__global__ void power(double *x, double *y, int n) {
  int index = threadIdx.x + blockIdx.x * blockDim.x;
  if (index < n) {
    double xi = x[index];
    y[index] = xi * (1 + xi * (1 + xi * (1 + xi * (1 + xi * (1 + xi * (1 + xi * (1 + xi)))))));
  }
}

// wall-clock time in seconds
double wtime(void) {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + 1e-6 * tv.tv_usec;
}

int main(void) {
  double *x, *y;      // host copies of x, y
  double *x_d, *y_d;  // device copies of x, y
  size_t size = (size_t)N * sizeof(double);
  double t0, t1;
  int i, k;

  // Alloc space for device copies of x, y
  cudaMalloc((void **)&x_d, size);
  cudaMalloc((void **)&y_d, size);

  // Alloc space for host copies of x, y and setup input values
  x = (double *)malloc(size);
  y = (double *)malloc(size);
  for (i = 0; i < N; i++) x[i] = rand() / (double)RAND_MAX;

  // Copy input to device (only once: transfers over the PCI bus are slow)
  t0 = wtime();
  cudaMemcpy(x_d, x, size, cudaMemcpyHostToDevice);
  t1 = wtime();
  printf("Starting with %d blocks of %d threads\n",
         (N + BLOCKSIZE - 1) / BLOCKSIZE, BLOCKSIZE);
  printf("copy x to device time (ms): %f\n", 1000 * (t1 - t0));

  for (k = 0; k < 4; k++) {
    t0 = wtime();
    // Launch power() kernel on GPU
    power<<<(N + BLOCKSIZE - 1) / BLOCKSIZE, BLOCKSIZE>>>(x_d, y_d, N);
    // Kernel launches are asynchronous: wait for the GPU to finish
    cudaDeviceSynchronize();
    t1 = wtime();
    // Copy one element of the result back to host for printing
    cudaMemcpy(&y[k], &y_d[k], sizeof(double), cudaMemcpyDeviceToHost);
    printf("pass %d time (ms): %f %f\n", k + 1, 1000 * (t1 - t0), y[k]);
  }

  // Check for errors (from the API calls or from the kernels)
  printf("%s\n", cudaGetErrorString(cudaGetLastError()));

  // Copy the full result back to host
  t0 = wtime();
  cudaMemcpy(y, y_d, size, cudaMemcpyDeviceToHost);
  t1 = wtime();
  printf("copy y to host time (ms): %f\n", 1000 * (t1 - t0));

  // Cleanup
  free(x); free(y);
  cudaFree(x_d); cudaFree(y_d);
  return 0;
}
