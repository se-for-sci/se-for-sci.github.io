program compute_pi
  ! Declare and/or Initialize variables
  use mpi
  implicit none
  real(kind=8) :: pi = 4.d0*ATAN(1.d0)

  integer :: narg, info, myid, ncpu
  integer(kind=8) :: i, n, imin, imax
  real(kind=8) :: h = 1
  real(kind=8) :: strt, stop, x, integ, integ_tot
  character(len=80) :: arg

  ! MPI init
  call MPI_INIT(info)
  call MPI_COMM_SIZE(MPI_COMM_WORLD,ncpu,info)
  call MPI_COMM_RANK(MPI_COMM_WORLD,myid,info)

  ! Parse input
  narg = command_argument_count()
  if (narg .eq. 0) then
     n = int(1e10,kind=8)
  else if (narg .eq. 1) then
     call get_command_argument(1, arg)
     read(arg,*) n
  else
     if(myid==1)then
        write(*,*)  'Usage: ./compute_pi [n]'
     endif
     call exit(1)
  end if

  h = 1d0/dble(n)

  if(myid==1)then
     write(*,*)'Starting with ',ncpu,' tasks'
  end if

  call cpu_time(strt)

  imin = int(myid*dble(n)/dble(ncpu),kind=8)+1
  imax = int((myid+1)*dble(n)/dble(ncpu),kind=8)

  integ = 0d0
  do i = imin, imax
     x = dble(i)/dble(n)
     integ = integ + 1d0/(1d0+x**2)*h
  end do

  call MPI_ALLREDUCE(integ,integ_tot,1,MPI_DOUBLE_PRECISION,MPI_SUM,MPI_COMM_WORLD,info)

  call cpu_time(stop)

  ! Print result and timing
  if(myid==1)then
     write(*,*)4*integ_tot, PI, PI-4*integ_tot
     write(*,'(A, ES13.6, A)') 'Finished in ', stop-strt, ' s'
  endif

  call MPI_FINALIZE(info)

end program compute_pi
