#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import hashlib
from Crypto.PublicKey import RSA
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



class Alice():
	def __init__(self):
		self.banknot = []
		self.M = None

	def generuj_100_banknotow(self,kwota):
		for i in range(1,101):
			self.banknot.append(Banknot(kwota))

	def zakryj_banknoty(self,bank):
		for obecny_banknot in self.banknot:
			obecny_banknot.zakryj_banknot(bank)

	def odkryj_podpis(self,bank):
		for obecny_banknot in self.banknot:
			obecny_banknot.ujawnij_Z()
			obecny_banknot.podpis_S = bank.klucz_publiczny.unblind(obecny_banknot.podpis_S_zakryty[0], obecny_banknot.ciag_Z_ujawniony)
	
	def odbierz_bity(self,sprzedawca):
		self.bity = sprzedawca.bity



class Bank():
	def __init__(self):
		self.__klucz_prywatny = RSA.generate(2048)
		self.klucz_publiczny = self.__klucz_prywatny.publickey()
		self.banknot = []

		self.depozyt = []
		self.depozyt_S = []
		self.depozyt_B = []
		self.depozyt_L = []
		self.depozyt_T = []
		self.depozyt_C = []
		self.depozyt_R = []

	def odbierz_banknoty(self,banknot):
		self.banknot = banknot

	def odkryj_banknoty(self):
		self.wyklucz = random.randint(0, 99)
		for index,obecny_banknot in enumerate(self.banknot):
			if index != self.wyklucz:
				obecny_banknot.ujawnij_B()
				obecny_banknot.ujawnij_L()
				obecny_banknot.ujawnij_Z()
				obecny_banknot.ujawnij_C()
				obecny_banknot.ujawnij_R()
				obecny_banknot.M_odkryte = self.klucz_publiczny.unblind(obecny_banknot.Y[0] , obecny_banknot.ciag_Z_ujawniony)

	def sprawdz_banknoty(self):
		identyfikatory = []
		rozne_identyfikatory = True
		sprawdzone_Y = True
		zobowiazanie_L = True
		zobowiazanie_R = True

		for index,obecny_banknot in enumerate(self.banknot):
			if index != self.wyklucz:
				#Sprawdzamy czy identyfikatory są różne
				if obecny_banknot.identyfikator in identyfikatory:
					rozne_identyfikatory = False
				else:
					identyfikatory.append(obecny_banknot.identyfikator)
				#Sprawdzamy czy Y są takie same
				if obecny_banknot.Y != obecny_banknot.Y:
					sprawdzone_Y = False
				#Sprawdzamy zobowiązanie bitowe dla L
				obecny_banknot.U2 = obecny_banknot.hashuj(obecny_banknot.ciag_S,obecny_banknot.ciag_B_ujawniony, obecny_banknot.ciag_L_ujawniony)
				if obecny_banknot.U2 != obecny_banknot.ciag_U and obecny_banknot.ciag_S != obecny_banknot.ciag_S:
					zobowiazanie_L = False
				#Sprawdzamy zobowiązanie bitowe dla R
				obecny_banknot.W2 = obecny_banknot.hashuj(obecny_banknot.ciag_T,obecny_banknot.ciag_C_ujawniony, obecny_banknot.ciag_R_ujawniony)
				if obecny_banknot.W2 != obecny_banknot.ciag_W and obecny_banknot.ciag_T != obecny_banknot.ciag_T:
					zobowiazanie_T = False



		if rozne_identyfikatory:
			print "Wszystkie identyfikatory różnią się od siebie."
		else:
			print "Identyczne identyfikatory w banknotach!"

		if sprawdzone_Y:
			print "Wszystkie banknoty mają identyczną zawartość Y."
		else:
			print "Zawartość Y w banknotach nie zgadza się!"

		if zobowiazanie_L:
			print "Zobowiazanie bitowe dla L zgadza się."
		else: 
			print "Zobowiazanie bitowe dla L NIE zgadza się!"

		if zobowiazanie_R:
			print "Zobowiazanie bitowe dla R zgadza się."
		else: 
			print "Zobowiazanie bitowe dla R NIE zgadza się!"


	def zloz_slepy_podpis(self):
		for obecny_banknot in self.banknot:
			obecny_banknot.podpis_S_zakryty = self.__klucz_prywatny.sign(obecny_banknot.Y, 0)

	def weryfikuj_podpis(self):
		weryfikacja = True
		for obecny_banknot in self.banknot:
			if not self.klucz_publiczny.verify(obecny_banknot.M_ujawniony, ((obecny_banknot.podpis_S,))):
				weryfikacja = False
		if weryfikacja:
			print "Bank zaakceptował wszystkie podpisy od sprzedawcy."
		else:
			print "Bank NIE zaakceptował podpisów banku!"

	def zdeponuj_banknot(self):
		brak_niezgodnosci = True
		for obecny_banknot in self.banknot:
			if obecny_banknot.identyfikator not in self.depozyt:
				self.depozyt.append(obecny_banknot.identyfikator)
				self.depozyt_S.append(obecny_banknot.S)
				if not hasattr(obecny_banknot, 'ciag_B_ujawniony'):
					obecny_banknot.ujawnij_B()
				self.depozyt_B.append(obecny_banknot.ciag_B_ujawniony)
				if not hasattr(obecny_banknot, 'ciag_L_ujawniony'):
					obecny_banknot.ujawnij_L()
				self.depozyt_L.append(obecny_banknot.ciag_L_ujawniony)
				self.depozyt_T.append(obecny_banknot.ciag_T)
				if not hasattr(obecny_banknot, 'ciag_C_ujawniony'):
					obecny_banknot.ujawnij_C()
				self.depozyt_C.append(obecny_banknot.ciag_C_ujawniony)
				if not hasattr(obecny_banknot, 'ciag_R_ujawniony'):
					obecny_banknot.ujawnij_R()
				self.depozyt_R.append(obecny_banknot.ciag_R_ujawniony)
			else:
				brak_niezgodnosci = False

		if brak_niezgodnosci:
			print "Bank zdeponował udanie wszystkie banknoty."
		else:
			print "Wykryto próbę podwójnego użycia banknotów!"



class Sprzedawca():
	def __init__(self):
		self.klucz_publiczny = None
		self.bity = []

	def odbierz_podpisane_banknoty(self,banknot):
		self.banknot = banknot
		for obecny_banknot in banknot:
			obecny_banknot.ujawnij_M()

	def pobierz_klucz_publiczny(self,bank):
		self.klucz_publiczny = bank.klucz_publiczny

	def weryfikuj_podpis(self):
		weryfikacja = True
		for obecny_banknot in self.banknot:
				if not self.klucz_publiczny.verify(obecny_banknot.M_ujawniony, ((obecny_banknot.podpis_S,))):
					weryfikacja = False
		if weryfikacja:
			print "Sprzedawca zaakceptował wszystkie podpisy Alice."
		else:
			print "Sprzedawca NIE zaakceptował podpisów Alice!"

	def generuj_100_bitow(self):
		for i in range(1,101):
			self.bity.append(random.getrandbits(1))

	def sprawdz_zobowiazanie(self):
		zobowiazanie_L = True
		zobowiazanie_R = True
		for index,obecny_banknot in enumerate(self.banknot):
			if self.bity[index] == 0:
				#Sprawdzamy zobowiązanie bitowe dla prawej połowy
				obecny_banknot.ujawnij_B()
				obecny_banknot.ujawnij_L()
				obecny_banknot.U2 = obecny_banknot.hashuj(obecny_banknot.ciag_S,obecny_banknot.ciag_B_ujawniony, obecny_banknot.ciag_L_ujawniony)
				if obecny_banknot.U2 != obecny_banknot.ciag_U and obecny_banknot.ciag_S != obecny_banknot.ciag_S:
					zobowiazanie_L = False

			elif self.bity[index] == 1:
				#Sprawdzamy zobowiązanie bitowe dla lewej połowy
				obecny_banknot.ujawnij_C()
				obecny_banknot.ujawnij_R()
				obecny_banknot.W2 = obecny_banknot.hashuj(obecny_banknot.ciag_T,obecny_banknot.ciag_C_ujawniony, obecny_banknot.ciag_R_ujawniony)
				if obecny_banknot.W2 != obecny_banknot.ciag_W and obecny_banknot.ciag_T != obecny_banknot.ciag_T:
					zobowiazanie_T = False

		if zobowiazanie_L:
			print "Zobowiazanie bitowe dla L zgadza się."
		else: 
			print "Zobowiazanie bitowe dla L NIE zgadza się!"

		if zobowiazanie_R:
			print "Zobowiazanie bitowe dla R zgadza się."
		else: 
			print "Zobowiazanie bitowe dla R NIE zgadza się!"



# Tworzymy bank i Alice
bank = Bank()
alice = Alice()
sprzedawca = Sprzedawca()

#Alice tworzy 100 banknotów
alice.generuj_100_banknotow(100)

#Alice zakrywa banknoty
alice.zakryj_banknoty(bank)

#Alice wysyła wszystkie 100 banknotów ZAKRYTYCH do banku
bank.odbierz_banknoty(alice.banknot)

#Alice ujawnia 99 banknotów poza j-tym
bank.odkryj_banknoty()

#Bank sprawdza 99 banknotów
bank.sprawdz_banknoty()

#Bank ślepo podpisuje wszystkie banknoty
bank.zloz_slepy_podpis()

#Alice odkrywa banknoty
alice.odkryj_podpis(bank)

#Sprzedawca odbiera banknoty wraz z ich podpisami
sprzedawca.odbierz_podpisane_banknoty(alice.banknot)

#Sprzedawca pobiera klucz publiczny banku
sprzedawca.pobierz_klucz_publiczny(bank)

#Sprzedawca weryfikuje podpis
sprzedawca.weryfikuj_podpis()

#Sprzedawca generuj 100 losowych bitów
sprzedawca.generuj_100_bitow()

#Alice odbiera bity
alice.odbierz_bity(sprzedawca)

#Alice w zależności od wartości bitów ujawnia zobowiazanie bitowe
sprzedawca.sprawdz_zobowiazanie()

#Sprzedawca wysyła banknoty do banku, który weryfikuje podpis
bank.weryfikuj_podpis()

#Bank deponuje banknoty o ile nie zostały już wcześniej użyte
bank.zdeponuj_banknot()

