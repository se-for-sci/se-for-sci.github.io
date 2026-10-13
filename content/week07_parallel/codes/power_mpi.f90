program power
  use mpi
  implicit none

  integer, parameter :: n=100000000
  real(kind=8), allocatable :: x(:), y(:)
  real(kind=8) :: t0, t1, dt, dt_max
  integer :: i, k, info, myid, ncpu, imin, imax, nloc

  ! MPI init
  call MPI_INIT(info)
  call MPI_COMM_SIZE(MPI_COMM_WORLD,ncpu,info)
  call MPI_COMM_RANK(MPI_COMM_WORLD,myid,info)

  ! Each task only owns its own part of the arrays
  imin = int(myid*dble(n)/dble(ncpu))+1
  imax = int((myid+1)*dble(n)/dble(ncpu))
  nloc = imax-imin+1

  allocate(x(nloc), y(nloc))
  call random_number(x)

  if(myid==0)then
     write(*,*)'Starting with ',ncpu,' tasks'
  end if

  do k=1,4
     call MPI_BARRIER(MPI_COMM_WORLD,info)
     t0 = MPI_WTIME()
     do i=1,nloc
        y(i)=x(i)*(1+x(i)*(1+x(i)*(1+x(i)*(1+x(i)*(1+x(i)*(1+x(i)*(1+x(i))))))))
     enddo
     t1 = MPI_WTIME()
     ! The pass is finished when the slowest task is finished
     dt = t1-t0
     call MPI_REDUCE(dt,dt_max,1,MPI_DOUBLE_PRECISION,MPI_MAX,0,MPI_COMM_WORLD,info)
     if(myid==0)then
        write(*,*)'pass',k,'time (ms):',1000*dt_max,y(k)
     end if
  enddo

  call MPI_FINALIZE(info)

end program power
