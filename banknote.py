#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import random
from random import SystemRandom


# - Zawierają podpis elektroniczny – nie można powielić
# - Łatwo można je przesyłać drogą elektroniczną
# - Protokół obrotu cyfrowymi banknotami zapewniają pełną anonimowość strony, które postępuje zgodnie z protokołem
# - Banknoty można łatwo kopiować dlatego osoba która wykorzystała jeden banknote dwukrotnie ostanie wykrya
class Banknote():
    def __init__(self, amount_y):
        # Alice ustala kwotę Y
        self.amountY = amount_y

        # Losowy identifkator banknotu Xi [1,100]
        self.identity_x = random.getrandbits(100)


        # Losujemy nasz ciąg identyfikacyjny, do niego klucz R i dajemy do nich XOR który przypisujemy do L
        self.__string_R = random.getrandbits(100)
        self.__string_identity = random.getrandbits(100)  # __ => private
        self.__string_L = self.xor()

        # zobowiazenie dla L
        self.__string_B = random.getrandbits(100)
        self.string_S = random.getrandbits(100)
        self.string_U = self.hashuj(self.string_S, self.__string_B, self.__string_L)

        # zobowiazenie dla R

        self.__string_C = random.getrandbits(100)

        self.string_T = random.getrandbits(100)
        self.string_W = self.hashuj(self.string_T, self.__string_C, self.__string_R)

        # Klucz publiczny banku
        self.klucz_publiczny = None

        # Slepy podpis
        self.Z = None
        self.Y = None
        self.M_odkryte = None
        self.W2 = None
        self.V = None
        self.S = None

    def xor(self):
        return "".join(
            [chr(ord(c1) ^ ord(c2)) for (c1, c2) in zip(str(self.__string_identity), str(self.__string_R))])

    # return bytearray(a^b for a, b in zip(*map(bytearray, [self.__string_identity , self.__string_R])))

    def hashuj(self, string_1, string_2, string_3):
        hash = hashlib.sha256()
        hash.update(str(string_1))
        hash.update(str(string_2))
        hash.update(str(string_3))
        return hash

    def blind_banknote(self, bank):
        # pobieramy klucz publiczny banku
        self.klucz_publiczny = bank.klucz_publiczny
        # protokół ślepego podpisu
        self.__Z = SystemRandom().randrange(self.klucz_publiczny.n >> 10, self.klucz_publiczny.n)
        self.__M = str(self.amountY) + "|" + str(self.identity_x) + "|" + str(self.string_T) + "|" + str(
            self.string_W) + "|" + str(self.string_S) + "|" + str(self.string_U)
        self.Y = self.klucz_publiczny.blind(self.__M, self.__Z)

    def ujawnij_B(self):
        self.string_B_ujawniony = self.__string_B

    def ujawnij_L(self):
        self.string_L_ujawniony = self.__string_L

    def ujawnij_C(self):
        self.string_C_ujawniony = self.__string_C

    def ujawnij_R(self):
        self.string_R_ujawniony = self.__string_R

    def ujawnij_Z(self):
        self.string_Z_ujawniony = self.__Z

    def ujawnij_M(self):
        self.M_ujawniony = self.__M
