'''
author: Jacob Egner
date: 2015-08-01
island: electronic station

puzzle URLs:
http://www.checkio.org/mission/simplification/
https://github.com/Bryukh-Checkio-Tasks/checkio-task-simplification

for latest versions of my solutions, see my checkio solution github repo:
https://github.com/jmegner/CheckioPuzzles
'''


import collections


# inherited Counter maps power to coefficient
class Poly(collections.Counter):

    def __str__(self):
        exprStr = ""

        for power, coeff in reversed(sorted(self.items())):
            if coeff == 0:
                continue

            if power == 0:
                exprStr += "{:+}".format(coeff)

            else:
                if abs(coeff) == 1:
                    exprStr += "+x" if coeff == 1 else "-x"
                else:
                    exprStr += "{:+}*x".format(coeff)

                if power != 1:
                    exprStr += "**" + str(power)

        if exprStr:
            if exprStr[0] == "+":
                return exprStr[1:]
            return exprStr

        return "0"


    def __neg__(self):
        negatedPoly = Poly()

        for power, coeff in self.items():
            negatedPoly[power] = -coeff

        return negatedPoly


    def __add__(self, other):
        if isinstance(other, int):
            return self + Poly({0 : other})

        addedPoly = self.copy()
        addedPoly.update(other)
        return addedPoly


    def __sub__(self, other):
        return self + -other


    def __rsub__(self, other):
        return other + -self


    def __mul__(self, other):
        if isinstance(other, int):
            return self * Poly({0 : other})

        multedPoly = Poly()

        for power1, coeff1 in self.items():
            for power2, coeff2 in other.items():
                multedPoly[power1 + power2] += coeff1 * coeff2

        return multedPoly


    __radd__ = __add__
    __rmul__ = __mul__


def simplify(exprStr):
    x = Poly({1 : 1})
    exprPoly = eval(exprStr)
    return str(exprPoly)


if __name__ == "__main__":
    assert simplify("(x-1)*(x+1)") == "x**2-1", "First and simple"
    assert simplify("(x+1)*(x+1)") == "x**2+2*x+1", "Almost the same"
    assert simplify("(x+3)*x*2-x*x") == "x**2+6*x", "Different operations"
    assert simplify("x+x*x+x*x*x") == "x**3+x**2+x", "Don't forget about order"
    assert simplify("(2*x+3)*2-x+x*x*x*x") == "x**4+3*x+6", "All together"
    assert simplify("x*x-(x-1)*(x+1)-1") == "0", "Zero"
    assert simplify("5-5-x") == "-x", "Negative C1"
    assert simplify("x*x*x-x*x*x-1") == "-1", "Negative C0"

