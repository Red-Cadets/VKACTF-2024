import random
import functools

class FSS():
    def __init__(self, minimum, shares):
        self.minimum = minimum
        self.shares = shares
       
        self.PRIME = 2 ** 521 - 1  # 13th Mersenne Prime
        self.RINT = functools.partial(random.SystemRandom().randint, 0)

    def eval_at(self,poly, x, prime):

        accum = 0
        for coeff in reversed(poly):
            accum *= x
            accum += coeff
            accum %= prime
        return accum

    def make_random_shares(self,secret, minimum, shares, prime=2 ** 521 - 1, poly=None):

        if minimum > shares:
            raise ValueError("Pool secret would be irrecoverable.")
        if poly is None:
            poly = [secret] + [self.RINT(prime - 1) for _ in range(minimum - 1)]
        elif len(poly) == minimum-1:
            poly = [secret] + poly
        else:
            raise ValueError("Invalid poly")
        
        points = [(i, self.eval_at(poly, i, prime))
                for i in range(1, shares + 1)]
        return points, poly[1:]

    def extended_gcd(self,a, b):

        x = 0
        last_x = 1
        y = 1
        last_y = 0
        while b != 0:
            quot = a // b
            a, b = b, a % b
            x, last_x = last_x - quot * x, x
            y, last_y = last_y - quot * y, y
        return last_x, last_y

    def divmod(self,num, den, p):

        inv, _ = self.extended_gcd(den, p)
        return num * inv

    def lagrange_interpolate(self,x, x_s, y_s, p):

        k = len(x_s)
        assert k == len(set(x_s)), "points must be distinct"
        def PI(vals):  
            accum = 1
            for v in vals:
                accum *= v
            return accum
        nums = []  
        dens = []
        for i in range(k):
            others = list(x_s)
            cur = others.pop(i)
            nums.append(PI(x - o for o in others))
            dens.append(PI(cur - o for o in others))
        den = PI(dens)
        num = sum([self.divmod(nums[i] * den * y_s[i] % p, dens[i], p)
                for i in range(k)])
        return (self.divmod(num, den, p) + p) % p

    def recover_secret(self, shares, prime=2 ** 521 - 1):

        if len(shares) < self.minimum:
            raise ValueError(f"need at least {self.minimum} shares")
        x_s, y_s = zip(*shares)
        return self.lagrange_interpolate(0, x_s, y_s, prime)

    def split(self, secret, poly):

        shares, poly = self.make_random_shares(secret, self.minimum, self.shares, poly=poly)
        return shares, poly

    def bind(self, shares):

        secret = self.recover_secret(shares[:self.minimum])
        return secret

