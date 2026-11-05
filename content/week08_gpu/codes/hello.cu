#include <stdio.h>

// kernel: runs on the device, called from the host
__global__ void mykernel(void) {
  printf("Hello World from the GPU!\n");
}

int main(void) {
  // Launch mykernel() on the GPU with 1 block of 1 thread
  mykernel<<<1, 1>>>();
  // Kernel launches are asynchronous: wait for the GPU to finish
  cudaDeviceSynchronize();
  printf("Hello World from the CPU!\n");

  // Check for errors (from the API calls or from the kernel)
  printf("%s\n", cudaGetErrorString(cudaGetLastError()));
  return 0;
}
