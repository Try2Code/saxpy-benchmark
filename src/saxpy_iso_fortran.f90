!make:nvfortran -cpp -DN=1000000000  -stdpar -Minfo=accel -gpu=cc80,cuda11.0 saxpy_iso_fortran.f90 -Wall  -o saxpy_iso_fortran

#ifndef N
#define N 2**20
#endif
subroutine saxpy(n,a,x,y)
  integer*8 :: n
  real :: a, x(n), y(n)
  
  integer*8 :: i
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
