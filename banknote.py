#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import random
from random import SystemRandom


class Banknot():
	def __init__(self, kwota):
		#Alice ustala kwotę
		self.kwota = kwota
		#Losujemy identyfikator
		self.identyfikator = random.getrandbits(100)
		#sekwencja dla ciągu identyfikacyjnego
		#Losujemy nasz ciąg identyfikacyjny, do niego klucz R i dajemy do nich XOR który przypisujemy do L
		self.__ciag_R = random.getrandbits(100)
		self.__ciag_identyfikacyjny = random.getrandbits(100)  #__ => private
		self.__ciag_L = self.xor()
		#sekwencja zobowiązań bitowych
		#zobowiazenie dla R
		self.ciag_T  = random.getrandbits(100)
		self.__ciag_C  = random.getrandbits(100)
		self.ciag_W = self.hashuj(self.ciag_T,self.__ciag_C,self.__ciag_R)
		#zobowiazenie dla L
		self.ciag_S  = random.getrandbits(100)
		self.__ciag_B  = random.getrandbits(100)
		self.ciag_U = self.hashuj(self.ciag_S,self.__ciag_B,self.__ciag_L)

		#Klucz publiczny banku
		self.klucz_publiczny = None
		
		#Slepy podpis
		self.Z = None
		self.Y = None

		self.M_odkryte = None

		self.U2 = None
		self.W2 = None

		self.V = None
		self.S = None




	def xor(self):
		return "".join([chr(ord(c1) ^ ord(c2)) for (c1,c2) in zip(str(self.__ciag_identyfikacyjny) , str(self.__ciag_R))])
		#return bytearray(a^b for a, b in zip(*map(bytearray, [self.__ciag_identyfikacyjny , self.__ciag_R])))

	def hashuj(self,ciag_1,ciag_2,ciag_3):
		hash = hashlib.sha256()
		hash.update(str(ciag_1))
		hash.update(str(ciag_2))
		hash.update(str(ciag_3))
		return hash

	def zakryj_banknot(self,bank):
		#pobieramy klucz publiczny banku
		self.klucz_publiczny = bank.klucz_publiczny
		#protokół ślepego podpisu
		self.__Z = SystemRandom().randrange(self.klucz_publiczny.n >> 10, self.klucz_publiczny.n)
		self.__M = str(self.kwota)+"|"+str(self.identyfikator)+"|"+str(self.ciag_T)+"|"+str(self.ciag_W)+"|"+str(self.ciag_S)+"|"+str(self.ciag_U)
		self.Y = self.klucz_publiczny.blind(self.__M, self.__Z)

	def ujawnij_B(self):
		self.ciag_B_ujawniony = self.__ciag_B

	def ujawnij_L(self):
		self.ciag_L_ujawniony = self.__ciag_L

	def ujawnij_C(self):
		self.ciag_C_ujawniony = self.__ciag_C

	def ujawnij_R(self):
		self.ciag_R_ujawniony = self.__ciag_R

	def ujawnij_Z(self):
		self.ciag_Z_ujawniony = self.__Z

	def ujawnij_M(self):
		self.M_ujawniony = self.__M
