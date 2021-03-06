import numpy as np


class NumMethods:
    """
    Methods of numerical differentiation and integration.

        - Differentiation: Forward differences, endpoint and midpoint 3 and 5 point differences,
                           second derivative midpoint

        - Integration: Trapezoid rule (composite), Simpson's rule (composite + adaptive),
                       Gaussian quadrature (adaptive)
    """

    def __init__(self, func=None):
        self.func = func

    def for_diff(self, x, h=10**(-5)):
        """
          Forward Differences: Approximates f'(x) using (f(x+h)-f(x))/h for very small h.

          Args:
              x (float): Approximation point
              h (float): Increment

          Returns:
              float: f'(x) approximation
          """
        return (self.func(x + h) - self.func(x))/h

    def end_3diff(self, x, h=10**(-5)):
        """
          Three-Point Endpoint: Approximates f'(x)

          Args:
              x (float): Approximation point
              h (float): Increment

          Returns:
              float: f'(x) approximation
          """
        return (-3*self.func(x) + 4*self.func(x+h) - self.func(x+2*h))/(2*h)

    def mid_3diff(self, x, h=10**(-5)):
        """
          Three-Point Midpoint: Approximates f'(x)

          Args:
              x (float): Approximation point
              h (float): Increment

          Returns:
              float: f'(x) approximation
          """
        return (self.func(x+h) - self.func(x-h))/(2*h)

    def end_5diff(self, x, h=10**(-5)):
        """
          Five-Point Endpoint: Approximates f'(x)

          Args:
              x (float): Approximation point
              h (float): Increment

          Returns:
              float: f'(x) approximation
          """
        return (-25*self.func(x) + 48*self.func(x+h) - 36*self.func(x+2*h) +
                16*self.func(x+3*h) - 3*self.func(x+4*h))/(12*h)

    def mid_5diff(self, x, h=10**(-5)):
        """
          Five-Point Midpoint: Approximates f'(x)

          Args:
              x (float): Approximation point
              h (float): Increment

          Returns:
              float: f'(x) approximation
          """
        return (self.func(x-2*h) - 8*self.func(x-h) + 8*self.func(x+h) -
                self.func(x+2*h))/(12*h)

    def second_diff(self, x, h=10**(-5)):
        """
          Second Derivative Midpoint: Approximates f''(x)

          Args:
              x (float): Approximation point
              h (float): Increment

          Returns:
              float: f''(x) approximation
          """
        return (self.func(x-h) - 2*self.func(x) + self.func(x+h))/(h**2)

    def trapezoid_rule(self, a, b):
        """
          Approximate area under f(x) within [a,b] using a trapezoid.

          Args:
              a (float): Defines [a,b] integration bounds
              b (float): Defines [a,b] integration bounds

          Returns:
              float: int_(a,b)f(x)dx approximation
          """
        return ((b-a)/2) * (self.func(a) + self.func(b))

    def trap_comp(self, a, b, n=10):
        """
          Composite trapezoid rule approximation of int_(a,b)f(x)dx by summing
          trapezoidal approximations for n sub intervals.

          Args:
              a (float): Defines [a,b] integration bounds
              b (float): Defines [a,b] integration bounds
              n (int): Number of sub intervals. Must be an even integer

          Returns:
              float: int_(a,b)f(x)dx approximation
          """
        h = (b-a)/n
        mid_terms = 0
        for i in range(n):
            mid_terms += self.func(a+i*h)
        return (h/2) * (self.func(a) + 2*mid_terms + self.func(b))

    def simpsons_rule(self, a, b):
        """
          Simpson's rule approximation of int_(a,b)f(x)dx.

          Args:
              a (float): Defines [a,b] integration bounds
              b (float): Defines [a,b] integration bounds

          Returns:
              float: int_(a,b)f(x)dx approximation
          """
        h = (b-a)/2
        return (h/3) * (self.func(a) + 4*self.func((b+a)/2) + self.func(b))

    def simp_comp(self, a, b, n=10):
        """
          Composite Simpson's rule approximation of int_(a,b)f(x)dx by applying
          Simpson's rule over n sub intervals.

          Args:
              a (float): Defines [a,b] integration bounds
              b (float): Defines [a,b] integration bounds
              n (int): Number of sub intervals. Must be an even integer

          Returns:
              float: int_(a,b)f(x)dx approximation
          """
        h = (b-a)/n
        x_0 = self.func(a) + self.func(b)
        x_odd = 0
        x_even = 0
        for i in range(1, n):
            x = a + i*h
            if i % 2 == 0:
                x_even += self.func(x)
            else:
                x_odd += self.func(x)
        xi = h*(x_0 + 2*x_even + 4*x_odd)/3
        return xi

    def simp_adpt(self, a, b, tol=10**(-5), n_0=20):
        """
          Adaptive Simpson's rule approximation of int_(a,b)f(x)dx.

          Args:
              a (float): Defines [a,b] integration bounds
              b (float): Defines [a,b] integration bounds
              tol (float): Error tolerance
              n_0 (int): Max sub interval depth

          Returns:
              float: int_(a,b) f(x)dx approximation
          """
        approx = 0
        i = 0
        e, a0, h, fa, fc, fb, s, l = np.zeros((8, n_0))
        e[i] = 10*tol
        a0[i] = a
        h[i] = (b-a)/2
        fa[i] = self.func(a)
        fc[i] = self.func(a+h[i])
        fb[i] = self.func(b)
        s[i] = h[i]*(fa[i] + 4*fc[i] + fb[i])/3
        l[i] = 1
        while i > -1:
            fd = self.func(a0[i] + h[i]/2)
            fe = self.func(a0[i] + 3*h[i]/2)
            s1 = h[i]*(fa[i] + 4*fd + fc[i])/6
            s2 = h[i]*(fc[i] + 4*fe + fb[i])/6
            v1 = a0[i]
            v2 = fa[i]
            v3 = fc[i]
            v4 = fb[i]
            v5 = h[i]
            v6 = e[i]
            v7 = s[i]
            v8 = l[i]
            i -= 1

            if abs(s1 + s2 - v7) < v6:
                approx += s1 + s2
            elif v8 >= n_0:
                print("Level exceeded")
                return approx
            else:
                i += 1

                a0[i] = v1 + v5
                fa[i] = v3
                fc[i] = fe
                fb[i] = v4
                h[i] = v5/2
                e[i] = v6/2
                s[i] = s2
                l[i] = v8 + 1

                i += 1

                a0[i] = v1
                fa[i] = v2
                fc[i] = fd
                fb[i] = v3
                h[i] = h[i-1]
                e[i] = e[i-1]
                s[i] = s1
                l[i] = l[i-1]
        return approx

    def gquad(self, a, b):
        """
          Two-point Gaussian quadrature formula for approximating int_(a,b)f(x)dx where
          [a,b] is a general interval. Derived from the approximation
          int_(-1,1) f(x)dx (approximately)= f( -sqrt(3)/3 ) - f( sqrt(3)/3 )

          Args:
              a (float): Defines [a,b] integration bounds
              b (float): Defines [a,b] integration bounds

          Returns:
              float: int_(a,b)f(x)dx approximation
          """
        return (self.func((1/2) * ((b-a) * (-np.sqrt(3)/3) + a+b)) +
                self.func((1/2) * ((b-a) * (np.sqrt(3)/3) + a+b))) * (b-a)/2

    def gquad_adpt(self, a, b, level=0, current_sum=0, n_0=20, tol=10**(-7)):
        """
          Adaptive two-point Gaussian quadrature. Applies two-point Gaussian quadrature on sub intervals
          from splitting [a,b] until specified level of precision is reached.

          Args:
              a (float): Defines [a,b] integration bounds
              b (float): Defines [a,b] integration bounds
              level (int): Counts interval split depth
              current_sum (float): Current interval approximation
              n_0 (int): Max depth
              tol (float): Error tolerance

          Returns:
              float: int_(a,b)f(x)dx approximation
          """
        level += 1
        one_gauss = self.gquad(a, b)
        c = (a+b)/2
        two_gauss = self.gquad(a, c) + self.gquad(c, b)
        if level > n_0:
            print("Max depth reached")
        else:
            if abs(one_gauss - two_gauss) < tol:
                current_sum += two_gauss
            else:
                current_sum = self.gquad_adpt(a, c, level=level, current_sum=current_sum, n_0=n_0)
                current_sum = self.gquad_adpt(c, b, level=level, current_sum=current_sum, n_0=n_0)
        return current_sum
