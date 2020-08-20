from math import *
import numpy as np


def ln(n):
    return log(n, e)


class Dual(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(self.a + other, self.b)
        elif isinstance(other, Dual):
            return Dual(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(self.a - other, self.b)
        elif isinstance(other, Dual):
            return Dual(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(self.a * other, self.b * other)
        elif isinstance(other, Dual):
            return Dual(self.a * other.a, self.a * other.b + self.b * other.a)

    def __truediv__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return Dual(self.a / other, self.b / other)
        elif isinstance(other, Dual):
            if other.a == 0 and other.b == 0:
                raise ZeroDivisionError('Dual number divisor must be non-zero')
            elif other.a != 0:
                return self * other ** -1
                # return Dual(self.a / other.a, ((self.b + other.a) - (self.a + other.b)) / other.a ** 2)
            elif other.a == 0 and self.a == 0:
                return Dual(self.b / other.b, 0)
            else:
                raise ValueError('No solution in dual numbers')

    def __pow__(self, power, modulo=None):
        if power == 0:
            return Dual(1, 0)
        return Dual(self.a ** power, power * self.a ** (power - 1) * self.b)

    def root(self, power):
        return Dual(self.a ** (1 / power), self.b / (power * (self.a ** (power - 1)) ** (1 / power)))

    def sin(self):
        return Dual(sin(self.a), self.b * cos(self.a))

    def cos(self):
        return Dual(cos(self.a), -self.b * sin(self.a))

    def tg(self):
        return Dual(tan(self.a), self.b / (cos(self.a) ** 2))

    def ctg(self):
        return self.tg() ** -1

    def log(self, n):
        return Dual(log(self.a, n), self.b / (self.a * ln(n)))

    def exponential(self, n):
        return Dual(n ** self.a, (n ** self.a) * ln(n) * self.b)

    def __str__(self):
        return f'{self.a} + {self.b} * eps'

    def __int__(self):
        return int(self.a)

    def __float__(self):
        return float(self.a)

    def __bool__(self):
        return not (self == Dual(0, 0))

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __neg__(self):
        return Dual(-self.a, -self.b)


def example(x):
    #return (x.exponential(2) - x ** 2).root(3)
    return x**3


EPSILON = Dual(0, 1)


def f(x):
    return EXP(x) / ((SIN(x) ** 3 + COS(x) ** 3) ** 0.5)


def deriv(f, x):
    # print(f(EPSILON + x) - f(x))
    return (f(EPSILON + x) - f(Dual(x, 0))).b


def old_deriv(f, x):
    dx = 1e-10
    df = f(x + dx) - f(x)
    return df / dx

print(deriv(example, 0))
# --------------------------------------------
# def root(number, power):
#     if isinstance(number, Dual):
#         return Dual(number.a ** (1 / power), number.b / (power * (number.a ** (power - 1)) ** (1 / power)))
#     else:
#         return number ** (1 / power)
#
#
# def LOG(number, power):
#     if isinstance(number, Dual):
#         return number.log(power)
#     else:
#         return log(number, power)
#
#
# def SIN(number):
#     if isinstance(number, Dual):
#         return number.sin()
#     else:
#         return sin(number)
#
#
# def COS(number):
#     if isinstance(number, Dual):
#         return number.cos()
#     else:
#         return cos(number)
#
#
# def CTAN(number):
#     if isinstance(number, Dual):
#         return number.ctg()
#     else:
#         return tan(number) ** -1
#
#
# def EXP(x):
#     if isinstance(x, Dual):
#         return x.exponential(e)
#     else:
#         return e ** x
#
#
# EPSILON = Dual(0, 1)
#
#
# def f(x):
#     return EXP(x) / ((SIN(x) ** 3 + COS(x) ** 3) ** 0.5)
#
#
# def deriv(f, x):
#     print(f(EPSILON + x) - f(x))
#     return (f(EPSILON + x) - f(x)).b
#
#
# def old_deriv(f, x):
#     dx = 1e-10
#     df = f(x + dx) - f(x)
#     return df / dx
#
#
# # print(A)
# # print(A + 2.0)
# #
# from time import time

# print((deriv(f, 1.5)))
# print(old_deriv(f, 1.5))
# # #
# t = time()
# for i in range(10 ** 5):
#     (deriv(f, 4))
# print(time() - t)
#
# t = time()
# for i in range(10 ** 5):
#     (old_deriv(f, 4))
# print(time() - t)
