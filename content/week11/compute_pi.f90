program compute_pi
  ! Declare and/or Initialize variables
  implicit none
  real(kind=8) :: pi = 4.d0*ATAN(1.d0)

  integer :: narg
  integer(kind=8) :: i, n
  real(kind=8) :: h = 1
  real(kind=8) :: strt, stop, x, integ
  character(len=80) :: arg
  
  ! Parse input
  narg = command_argument_count()
  if (narg .eq. 0) then
     n = int(1e10,kind=8)
  else if (narg .eq. 1) then
     call get_command_argument(1, arg)
     read(arg,*) n
  else
     write(*,*)  'Usage: ./compute_pi [n]'
     call exit(1)
  end if
  
  h = 1d0/dble(n)
  
  call cpu_time(strt)

  integ = 0d0
  do i = 1, n
     x = dble(i)/dble(n)
     integ = integ + 1d0/(1d0+x**2)*h
  end do

  call cpu_time(stop)

  ! Print result and timing
  write(*,*)4*integ, pi, pi-4*integ
  write(*,'(A, ES13.6, A)') 'Finished in ', stop-strt, ' s'
  
end program compute_pi
