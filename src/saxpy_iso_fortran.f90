
#ifndef N
#define N 2**20
#endif
subroutine saxpy(n,a,x,y)
  integer :: n
  real :: a, x(n), y(n)
  
  integer :: i
  do concurrent (i = 1: n)
  y(i) = a*x(i)+y(i)
  enddo
end subroutine saxpy

program main
  real :: x_d(N), y_d(N)
  x_d = 1.0
  y_d = 2.0

  print *, N

  call saxpy(N, 2.0, x_d, y_d)
end program main
