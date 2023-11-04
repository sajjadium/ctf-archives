module arrayops
  use types, only: dp
  implicit none
  private

  public :: arange, linspace, diff, midpoints, full, zeros, ones

contains

  pure function diff(x) result(r)
    real(dp), intent(in) :: x(:)
    real(dp) :: r(size(x)-1)
    integer :: i
    
    do i = 1, size(x)-1
      r(i) = x(i+1) - x(i)
    end do
  end function diff

  pure function midpoints(x) result(r)
    real(dp), intent(in) :: x(:)
    real(dp) :: r(size(x)-1)
    integer :: n
    n = size(x)
    r = (x(2:n) + x(1:n-1)) / 2.0_dp
  end function midpoints

  pure function arange(n) result(r)
    integer, intent(in) :: n
    real(dp) :: r(n)
    integer :: i
    r = [(real(i-1, dp), i=1,n)]
  end function arange

  pure function linspace(x_min, x_max, n) result(r)
    real(dp), intent(in) :: x_min, x_max
    integer, intent(in) :: n
    real(dp) :: r(n)

    r = x_min + (x_max-x_min)/(real(n, dp)-1.0_dp)*arange(n)
  end function linspace

  pure function full(n, s) result(r)
    integer, intent(in) :: n
    real(dp), intent(in) :: s
    real(dp) :: r(n)
    integer :: i

    r = [(s, i=1, n)]
  end function full

  pure function zeros(n) result(r)
    integer, intent(in) :: n
    real(dp) :: r(n)
    r = full(n, 0.0_dp)
  end function zeros

  pure function ones(n) result(r)
    integer, intent(in) :: n
    real(dp) :: r(n)
    r = full(n, 1.0_dp)
  end function ones
end module arrayops