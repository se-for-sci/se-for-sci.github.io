program poisson
  ! Declare and/or Initialize variables
  implicit none
  integer :: NDEF = 64
  integer :: MAXITER = 1000, OUTFREQ = 1000
  logical :: FOUT = .TRUE.

  integer :: n
  real(kind=8) :: h   = 1.
  real(kind=8) :: eps = 1.D-6

  real(kind=8), dimension(:,:), allocatable :: uold, unew, f

  integer           :: narg, i, j, iter = 0, nthreads
  real(kind=8)      :: x, y, err, terr, ffac, strt, stop, err0, ftot
  real(kind=8)      :: res, lap, omega = 1.0
  character(len=20) :: arg

  ! Parse input
  narg = command_argument_count()
  if (narg .eq. 0) then
    n = NDEF
  else if (narg .eq. 1) then
    call get_command_argument(1, arg)
    read(arg,*) n
  else if (narg .eq. 2) then
    call get_command_argument(1, arg)
    read(arg,*) n
    call get_command_argument(2, arg)
    read(arg,*) eps
  else
    write(*,*)  'Usage: ./poisson [n eps]'
    call exit(1)
  end if

  h = 1./n

  ! Allocate and fill the working arrays
  allocate(uold(0:n+1,0:n+1))
  allocate(unew(0:n+1,0:n+1))
  allocate(f(1:n,1:n))
  uold = 0.
  unew = 0.
  f = 0.

  ! Fill in the source function
  ftot = 0.
  do i = 1, n
     x = (i - .5) * h
     do j = 1, n
        y = (j - .5) * h
        f(i,j) = 0.0
        if(i .eq. n/2 .and. j .eq. n/2) f(i,j)=1.
        ftot = ftot + f(i,j)
     end do
  end do
  ftot = 0. !ftot/dble(n*n)

  ! Main loop
  ffac = h**2.
  err  = huge(err)
  call cpu_time(strt)

  do while((err .gt. eps) .and. (iter .lt. MAXITER))

     ! Jacobi method
     err = 0.

     do j = 1,n
        do i = 1,n

           lap = uold(i-1,j)+uold(i+1,j)+uold(i,j-1)+uold(i,j+1)-4.0*uold(i,j)
           res = lap - ffac * (f(i,j) - ftot)
           unew(i,j) = uold(i,j) + omega*0.25*res

           err = MAX(err,abs(unew(i,j) - uold(i,j)))
        end do
     end do

     ! Neumann boundary conditions
     do i = 1, n
        unew(i,0) = 0. !unew(i,n)
        unew(i,n+1) = 0. !unew(i,1)
        unew(0,i) = 0. !unew(n,i)
        unew(n+1,i) = 0. !unew(1,i)
     end do

     do j = 1,n
	do i = 1,n
           uold(i,j) = unew(i,j)
        end do
     end do

     iter = iter + 1
     if ((mod(iter,OUTFREQ) .eq. 0) .or. (err .lt. eps)) then
        write(*, '(A, I8, A, ES13.6)') 'Iter. ', iter, ', err = ', err
     end if

  end do

  ! Print timing
  call cpu_time(stop)

  write(*,'(A, ES13.6, A)') 'Finished in ', stop-strt, ' s'


  ! Final time step output
  if (FOUT) then
     open(7, file = 'final_phi.dat')
     write(7, *) n, eps, iter, err
     do i = 1, n
        write(7, '(*(ES13.6))') uold(i,1:n)
     end do
     close(7)
  end if

  deallocate(uold)
  deallocate(unew)
  deallocate(f)

end program poisson
