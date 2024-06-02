#!/usr/bin/ python3

import random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from os import urandom
from Crypto.Util.number import long_to_bytes, getPrime

class Utils():

    def linear_recurrence(self, m, n, initial_terms, coefficients):

        if len(initial_terms) != len(coefficients):
            raise ValueError("Число начальных членов и коэффициентов должно быть одинаковым")

        if n <= len(initial_terms):
            return initial_terms[n - 1]

        result = 0
        for i in range(len(initial_terms)):
            result += coefficients[i] * self.linear_recurrence(m, n - i - 1, initial_terms, coefficients) 

        return result % m

    
    def get_flag():

        return b'vka{???????????????????????????}'


class Alice():

    def __init__(self, m, SIZE, c, a):

        self.m = m
        self.SIZE = SIZE
        self.c = c
        self.a = a
        self.Utils = Utils()

    def gen_privkey(self, k):

        self.Na = random.randint(0, k)
        return self.Na

    def gen_pubkey(self):

        pub_a = [self.Utils.linear_recurrence(self.m, i + 1, self.a, self.c) for i in range(self.Na, self.Na + self.SIZE)]
        return pub_a
    
    def gen_secret(self, pub_b):

        S_a = [self.Utils.linear_recurrence(self.m, i + 1, pub_b, self.c) for i in range(self.Na, self.Na + self.SIZE)]
        return S_a

class Bob():

    def __init__(self, m, SIZE, c, a):

        self.m = m
        self.SIZE = SIZE
        self.c = c
        self.a = a
        self.Utils = Utils()

    def gen_privkey(self, k):

        self.Nb = random.randint(0, k)
        return self.Nb

    def gen_pubkey(self):

        pub_b = [self.Utils.linear_recurrence(self.m, i + 1, self.a, self.c) for i in range(self.Nb, self.Nb + self.SIZE)]

        return pub_b

    def gen_secret(self, pub_a):

        S_b = [self.Utils.linear_recurrence(self.m, i + 1, pub_a, self.c) for i in range(self.Nb, self.Nb + self.SIZE)]
        return S_b

def main():

    m = getPrime(128)
    SIZE = 20

    c = [random.randint(0, m) for _ in range(SIZE)]
    a = [random.randint(0, m) for _ in range(SIZE)]
    

    alice = Alice(m, SIZE, c, a)
    bob = Bob(m, SIZE, c, a)

    Na = alice.gen_privkey(m)
    Nb = bob.gen_privkey(m)

    pub_a = alice.gen_pubkey()
    pub_b = bob.gen_pubkey()

    S_a = alice.gen_secret(pub_b)
    S_b = bob.gen_secret(pub_a)

    assert S_a == S_b
    
    flag = Utils.get_flag()
    key = long_to_bytes(Na) 
    key = SHA256.new(data=str(key).encode()).digest()[:128]
    
    iv = urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(flag)

    params = {
        "m": m,
        "SIZE": SIZE,
        "c": c,
        "a": a
    }

    encrypted = {
        "iv": iv.hex(),
        "ciphertext": ciphertext.hex(),
        "Nb": Nb,
        "S_b": S_b
    }

    print(params)
    print(encrypted)

if __name__ == "__main__":
    main()