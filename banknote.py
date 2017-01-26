#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import random
from random import SystemRandom


# - Zawierają sign elektroniczny – nie można powielić
# - Łatwo można je przesyłać drogą elektroniczną
# - Protokół obrotu cyfrowymi banknotami zapewniają pełną anonimowość strony, które postępuje zgodnie z protokołem
# - Banknoty można łatwo kopiować dlatego osoba która wykorzystała jeden banknote dwukrotnie ostanie wykrya
class Banknote():
    BIT_COUNT = 100

    def __init__(self, amount_y):
        # Alice ustala kwotę Y
        self.amount_y = amount_y

        # Losowy identifkator banknotu Xi [1,100]
        self.identity_x = random.getrandbits(self.BIT_COUNT)

        # Losujemy nasz ciąg identyfikacyjny, do niego klucz R i dajemy do nich XOR który przypisujemy do L
        self.string_R = random.getrandbits(self.BIT_COUNT)
        self.string_identity = random.getrandbits(self.BIT_COUNT)  # __ => private

        # Alice oblicza Li, j = Ii, j XOR Rij
        self.string_L = self.xor()

        # zobowiazenie dla R
        # Alice losuje 2 ciągi Ti,j i Ci,j.
        # Liczba bitów powinna uniemożliwić znalezienie konfliktu dla H
        # Alice umieszcza ciągi wyżej napisane w banknocie a ciąg Ci,j zachowuje w sekrecie
        self.__string_C = random.getrandbits(self.BIT_COUNT)
        self.string_T = random.getrandbits(self.BIT_COUNT)
        self.string_W = self.one_way_hash_fun(self.string_T, self.__string_C, self.string_R)

        # zobowiazenie dla L
        # Alice losuje 2 ciągi Si,j i Bi,j Liczba bitów powinna uniemożliwiać znalezienie konfliktu dla H
        # Alice oblicza H(Si,j, Bi,j,Li,j) = Ui,j
        # Alice umieszcza ciągi Sij, Uij w banknocie a ciąg Bij zachowuje w sekrecie
        self.__string_B = random.getrandbits(self.BIT_COUNT)
        self.string_S = random.getrandbits(self.BIT_COUNT)
        self.string_U = self.one_way_hash_fun(self.string_S, self.__string_B, self.string_L)

        self.S = None

    def xor(self):
        return "".join(
            [chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(str(self.string_identity), str(self.string_R))])

    # return bytearray(a^b for a, b in zip(*map(bytearray, [self.string_identity , self.string_R])))
    @staticmethod
    def one_way_hash_fun(string_1, string_2, string_3):
        hash = hashlib.sha256()
        hash.update(str(string_1))
        hash.update(str(string_2))
        hash.update(str(string_3))
        return hash

    def blind_banknote(self, public_key):
        self.public_key = public_key
        # protokół ślepego signu
        self.__Z = SystemRandom().randrange(self.public_key.n >> 10, self.public_key.n)
        self.__M = str(self.amount_y) + "|" + str(self.identity_x) + "|" + str(self.string_T) + "|" + str(
            self.string_W) + "|" + str(self.string_S) + "|" + str(self.string_U)
        self.Y = self.public_key.blind(self.__M, self.__Z)

    def reveal_B(self):
        self.string_B_revealed = self.__string_B

    def reveal_L(self):
        self.string_L_revealed = self.string_L

    def reveal_C(self):
        self.string_C_revealed = self.__string_C

    def reveal_R(self):
        self.string_R_revealed = self.string_R

    def reveal_Z(self):
        self.string_Z_revealed = self.__Z

    def reveal_M(self):
        self.M_revealed = self.__M
