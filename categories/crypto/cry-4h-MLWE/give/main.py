from polynomials import *
from modules import *
from utils import *
import json
import os
import signal
import random

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

class Cipher():
    def __init__(self, q, n):
        self.q = q
        self.n = n
        self.R = PolynomialRing(self.q, self.n)
        self.M = Module(self.R)

    def ex_poly(self, poly, N=16):
        coeff_array = []
        for i in range(16):
            coeff_array.append(poly.__getitem__(i))
        return coeff_array

    def keygen(self):
        s0 = self.R.random_element_()
        s1 = self.R.random_element_()
        s = self.M([s0, s1]).transpose()
        A00 = self.R.random_element()
        A01 = self.R.random_element()
        A10 = self.R.random_element()
        A11 = self.R.random_element()
        A = self.M([[A00, A01], [A10, A11]])
        e0 = self.R.random_element_()
        e1 = self.R.random_element_()
        e = self.M([e0, e1]).transpose()
        t = A @ s + e
        return (A, t), s

    def encrypt(self, m, public_key):
        r0 = self.R.random_element_()
        r1 = self.R.random_element_()
        r = self.M([r0, r1]).transpose()
        e_10 = self.R.random_element_()
        e_11 = self.R.random_element_()
        e_1 = self.M([e_10, e_11]).transpose()
        e_2 = self.R.random_element_()
        A, t = public_key
        poly_m = self.R.decode(m).decompress(1)
        u = A.transpose() @ r + e_1
        v = (t.transpose() @ r)[0][0] + e_2 + poly_m  
        return u, v

    def decrypt(self, u, v, s):
        m_n = v - (s.transpose() @ u)[0][0]
        m_n_reduced = m_n.compress(1)
        return m_n_reduced.encode(l=1)

class Challenge():
    def __init__(self):
        self.cipher = Cipher(337, 16)

    def get_flag(self):
        return os.environ.get('FLAG')

    def challenge(self):
        print("Welcome to the Next Generation Challenge!")

        for i in range(5):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(120) 

            try:
                a = random.randint(0, 2**8 - 1)
                b = random.randint(0, 2**8 - 1)
                m = bytes([a, b])

                pub, priv = self.cipher.keygen()
                u, v = self.cipher.encrypt(m, pub)

                A1 = self.cipher.ex_poly(pub[0][0][0])
                A2 = self.cipher.ex_poly(pub[0][0][1])
                A3 = self.cipher.ex_poly(pub[0][1][0])
                A4 = self.cipher.ex_poly(pub[0][1][1])
                t1 = self.cipher.ex_poly(pub[1][0][0])
                t2 = self.cipher.ex_poly(pub[1][1][0])
                u1 = self.cipher.ex_poly(u[0][0])
                u2 = self.cipher.ex_poly(u[1][0])
                v0 = self.cipher.ex_poly(v)

                pub_key = json.dumps({"A": [A1, A2, A3, A4], "t": [t1, t2]})
                print(pub_key)

                ct = json.dumps({"u": [u1, u2], "v": v0})
                print(ct)

                n = self.cipher.decrypt(u, v, priv)
                assert m == n

                m_user = json.loads(input("\nEnter message in binary list: "))["m"]

                if m_user == bytes_to_bits(m):
                    print(f"\nCorrect! You solve the problem {i+1}/5")
                else:
                    print("\nWrong! Good luck next time!")
                    exit()
                
                signal.alarm(0)

            except TimeoutException:
                print("\nTime is up! Exiting...")
                exit()

        print("\nCongratulations! You have solved the challenge!")
        print(self.get_flag())
        exit()

if __name__ == '__main__':
    Challenge = Challenge()
    Challenge.challenge()
    exit()
