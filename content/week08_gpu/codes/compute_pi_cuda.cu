// Based on Tim Mattson's code for
// https://github.com/tgmattso/OpenMP_intro_tutorial
#include <cuda.h>
#include <stdio.h>
#include <sys/time.h>

#define NBLOCKS 1024
#define BLOCKSIZE 256

// parallel function: each thread computes a partial sum over many steps,
// then the threads of each block combine their partial sums
__global__ void compute_sum(long long num_steps, double step, double *sum) {
  __shared__ double temp[BLOCKSIZE];
  long long index = threadIdx.x + (long long)blockIdx.x * blockDim.x;
  long long stride = (long long)blockDim.x * gridDim.x;

  // Each thread handles the steps index, index+stride, index+2*stride, ...
  double partial = 0;
  for (long long i = index; i < num_steps; i += stride) {
    double x = (i + 0.5) * step;
    partial += 4.0 / (1.0 + x * x);
  }

  // Copy one partial sum per thread into shared memory
  temp[threadIdx.x] = partial;
  __syncthreads();

  // Tree reduction within the block
  for (int s = blockDim.x / 2; s > 0; s /= 2) {
    if (threadIdx.x < s)
      temp[threadIdx.x] += temp[threadIdx.x + s];
    __syncthreads();
  }

  // Thread 0 adds the partial sum of this block to the total
  if (threadIdx.x == 0)
    atomicAdd(sum, temp[0]);
}

// wall-clock time in seconds
double wtime(void) {
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return tv.tv_sec + 1e-6 * tv.tv_usec;
}

int main(void) {
  long long num_steps = 10000000000LL;
  double step = 1.0 / num_steps;
  double sum;     // host copy of sum
  double *sum_d;  // device copy of sum
  double t0, t1;

  // Alloc space for device copy of sum and set it to zero
  cudaMalloc((void **)&sum_d, sizeof(double));
  cudaMemset(sum_d, 0, sizeof(double));

  printf("Starting with %d blocks of %d threads\n", NBLOCKS, BLOCKSIZE);

  t0 = wtime();
  // Launch compute_sum() kernel on GPU
  compute_sum<<<NBLOCKS, BLOCKSIZE>>>(num_steps, step, sum_d);
  // Kernel launches are asynchronous: wait for the GPU to finish
  cudaDeviceSynchronize();
  t1 = wtime();

  // Copy result back to host
  cudaMemcpy(&sum, sum_d, sizeof(double), cudaMemcpyDeviceToHost);

  // Check for errors (from the API calls or from the kernel)
  printf("%s\n", cudaGetErrorString(cudaGetLastError()));

  double pi = step * sum;
  printf("pi is %f in %fs!\n", pi, t1 - t0);

  // Cleanup
  cudaFree(sum_d);
  return 0;
}
