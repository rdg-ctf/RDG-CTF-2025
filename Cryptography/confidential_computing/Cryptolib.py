def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

class Drob():
    def __init__(self, c, z):
        if c != 0:
            self.c = c
            self.z = z
        else:
            self.c = 0
            self.z = 1

    def Socr(self):
        if self.c != 0:
            d = gcd(self.c, self.z)
            self.c //= d
            self.z //= d
        else:
            self.z = 1

    def __repr__(self):
        return f'{self.c} / {self.z}'

    def __abs__(self):
        return Drob(abs(self.c), self.z)

    def __int__(self):
        return self.c // self.z

    def __eq__(self, other):
        if type(other) == int:
            if self.c % self.z == 0:
                return self.c // self.z == other
            else:
                return False
        self.Socr()
        other.Socr()
        return self.c == other.c and self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if type(other) == int:
            return self.c // self.z < other
        k = (self.z * other.z) // gcd(self.z, other.z)
        return self.c * (k // self.z) < other.c * (k // other.z)
    
    def __gt__(self, other):
        if type(other) == int:
            if self.c % self.z == 0:
                return self.c // self.z > other
            else:
                return self.c // self.z + 1 > other
        k = (self.z * other.z) // gcd(self.z, other.z)
        return self.c * (k // self.z) > other.c * (k // other.z)

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)

    def __pos__(self):
        return self

    def __neg__(self):
        return Drob(-self.c, self.z)

    def __add__(self, other):
        if type(other) == int:
            if other == 0:
                return self
            if self.c == 0:
                return Drob(other, 1)
            r = Drob(self.c + other*self.z, self.z)
            r.Socr()
            return r
        if self.c == 0:
            return other
        elif other.c == 0:
            return self
        z = (self.z * other.z) // gcd(self.z, other.z)
        c =  self.c * (z // self.z) + other.c * (z // other.z)
        r = Drob(c, z)
        r.Socr()
        return r

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if type(other) == int:
            if other == 0:
                return self
            if self.c == 0:
                return Drob(-other, 1)
            r = Drob(self.c - other*self.z, self.z)
            r.Socr()
            return r
        if self.c == 0:
            return -other
        elif other.c == 0:
            return self
        z = (self.z * other.z) // gcd(self.z, other.z)
        c =  self.c * (z // self.z) - other.c * (z // other.z)
        r = Drob(c, z)
        r.Socr()
        return r

    def __rsub__(self, other):
        return (-self).__sub__(-other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if type(other) == int:
            if other == 0:
                return Drob(0, 1)
            d = gcd(self.z, other)
            return Drob((other // d) * self.c, self.z // d)
        if self.c == 0 or other.c == 0:
            return Drob(0, 1)
        d1 = gcd(self.c, other.z)
        d2 = gcd(other.c, self.z)
        c = (self.c // d1) * (other.c // d2)
        z = (self.z // d2) * (other.z // d1)
        return Drob(c, z)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) == int:
            d = gcd(self.c, other)
            return Drob(self.c // d, self.z * (other // d))
        if self.c == 0:
            return Drob(0, 1)
        d1 = gcd(self.c, other.c)
        d2 = gcd(self.z, other.z)
        c = (self.c // d1) * (other.z // d2)
        z = (self.z // d2) * (other.c // d1)
        return Drob(c, z)

    def __rtruediv__(self, other):
        return Drob(self.z, self.c) * other

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __pow__(self, other):
        if other == 0:
            return Drob(1, 1)
        elif other > 0:
            s = self
        else:
            s = 1 / self
            other = -other
        Res = Drob(1, 1)
        for i in bin(other)[2:]:
            Res *= Res
            if i == '1':
                Res *= s
        return Res

    def __ipow__(self, other):
        return self.__pow__(other)
    
class Vector():
    def __init__(self, val):
        self.val = val

    def len_vec(self):
        return sum([self.val[i]**2 for i in range(len(self.val))])

    def __repr__(self):
        return str(self.val)

    def __eq__(self, other):
        return self.val == other.val

    def __ne__(self, other):
        return self.val != other.val

    def __pos__(self):
        return self

    def __neg__(self):
        return Vector([-v for v in self.val])

    def __add__(self, other):
        return Vector([self.val[i] + other.val[i] for i in range(len(self.val))])

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Vector([self.val[i] - other.val[i] for i in range(len(self.val))])

    def __isub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        if type(other) != Vector:
            return Vector([v*other for v in self.val])
        return sum([self.val[i] * other.val[i] for i in range(len(self.val))])

    def __rmul__(self, other):
        return self.__mul__(other)

def orto_GH(Matrix):
    n = len(Matrix)
    b = [0] * n
    B = [0] * n
    b[0] = Matrix[0]
    B[0] = b[0].len_vec()
    nu = [[Drob(0, 1) for i in range(len(b[0].val))] for _ in range(n)]
    for i in range(1, n):
        b[i] = Matrix[i]
        for j in range(i):
            nu[i][j] = (b[i] * b[j]) / B[j]
            b[i] = b[i] - b[j] * nu[i][j]
        B[i] = b[i].len_vec()
    return b, B, nu

def LLL_vector_drob(Matrix):
    _, B, nu = orto_GH(Matrix)
    n = len(Matrix)
    b = [Matrix[i] for i in range(n)]
    k = 1
    while k < n:
        if abs(nu[k][k-1]) > Drob(1, 2):
            if nu[k][k-1] > 0:
                r = int(Drob(1, 2) + nu[k][k-1])
            else:
                r = -int(Drob(1, 2) - nu[k][k-1])
            b[k] = b[k] - b[k-1]*r
            for j in range(k - 1):
                nu[k][j] = nu[k][j] - nu[k-1][j]*r
            nu[k][k-1] = nu[k][k-1] - r
        if B[k] < (Drob(3, 4) - nu[k][k-1]*nu[k][k-1]) * B[k-1]:
            nu1 = nu[k][k-1]
            B1 = B[k] + nu1*nu1*B[k-1]
            nu[k][k-1] = (nu1 * B[k-1]) / B1
            B[k] = (B[k-1] * B[k]) / B1
            B[k-1] = B1
            b[k-1], b[k] = b[k], b[k-1]
            if k > 1:
                for j in range(k - 1):
                    nu[k][j], nu[k-1][j] = nu[k-1][j], nu[k][j]
            for s in range(k + 1, n):
                t = nu[s][k]
                nu[s][k] = nu[s][k-1] - nu1*t
                nu[s][k-1] = t + nu[k][k-1]*nu[s][k]
            k = max(1, k - 1)
            continue
        if B[k] >= (Drob(3, 4) - nu[k][k-1]*nu[k][k-1]) * B[k-1]:
            for l in range(k - 2, -1, -1):
                if abs(nu[k][l]) > Drob(1, 2):
                    if nu[k][l] > 0:
                        r = int(Drob(1, 2) + nu[k][l])
                    else:
                        r = -int(Drob(1, 2) - nu[k][l])
                    b[k] = b[k] - b[l]*r
                    for j in range(l):
                        nu[k][j] = nu[k][j] - nu[l][j]*r
                    nu[k][l] = nu[k][l] - r
            k += 1
    return b

def LLL_drob(Matrix):
    n, m = len(Matrix), len(Matrix[0])
    b = [Vector([Matrix[i][j] for j in range(m)]) for i in range(n)]
    b = LLL_vector_drob(b)
    b = [[b[i].val[j] for j in range(m)] for i in range(n)]
    return b
    
def LLL(Matrix):
    n, m = len(Matrix), len(Matrix[0])
    b = [Vector([Drob(Matrix[i][j], 1) for j in range(m)]) for i in range(n)]
    b = LLL_vector_drob(b)
    b = [[b[i].val[j].c for j in range(m)] for i in range(n)]
    return b
