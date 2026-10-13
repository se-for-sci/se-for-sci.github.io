program power
  use omp_lib
  implicit none

  integer, parameter :: n=100000000
  real(kind=8), allocatable :: x(:), y(:)
  real(kind=8) :: t0, t1
  integer :: i, k

  allocate(x(n), y(n))
  call random_number(x)

  !$omp parallel
  !$omp master
  write(*,*)'Starting with ',omp_get_num_threads(),' threads'
  !$omp end master
  !$omp end parallel

  do k=1,4
     t0 = omp_get_wtime()
     !$omp parallel do
     do i=1,n
        y(i)=x(i)*(1+x(i)*(1+x(i)*(1+x(i)*(1+x(i)*(1+x(i)*(1+x(i)*(1+x(i))))))))
     enddo
     !$omp end parallel do
     t1 = omp_get_wtime()
     write(*,*)'pass',k,'time (ms):',1000*(t1-t0),y(k)
  enddo

end program power
