#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from Crypto.PublicKey import RSA


class Bank():
    def __init__(self):
        self.__klucz_prywatny = RSA.generate(2048)
        self.klucz_publiczny = self.__klucz_prywatny.publickey()
        self.banknote = []

        self.depozyt = []
        self.depozyt_S = []
        self.depozyt_B = []
        self.depozyt_L = []
        self.depozyt_T = []
        self.depozyt_C = []
        self.depozyt_R = []

    def receive_banknotes(self, banknot):
        self.banknote = banknot

    def unblind_banknotes(self):
        self.wyklucz = random.randint(0, 99)
        for index, obecny_banknot in enumerate(self.banknote):
            if index != self.wyklucz:
                obecny_banknot.ujawnij_B()
                obecny_banknot.ujawnij_L()
                obecny_banknot.ujawnij_Z()
                obecny_banknot.ujawnij_C()
                obecny_banknot.ujawnij_R()
                obecny_banknot.M_odkryte = self.klucz_publiczny.unblind(obecny_banknot.Y[0],
                                                                        obecny_banknot.string_Z_ujawniony)

    def check_banknotes(self):
        identyfikatory = []
        rozne_identyfikatory = True
        sprawdzone_Y = True
        zobowiazanie_L = True
        zobowiazanie_R = True

        for index, obecny_banknot in enumerate(self.banknote):
            if index != self.wyklucz:
                # Sprawdzamy czy identyfikatory są różne
                if obecny_banknot.identity_x in identyfikatory:
                    rozne_identyfikatory = False
                else:
                    identyfikatory.append(obecny_banknot.identity_x)
                # Sprawdzamy czy Y są takie same
                if obecny_banknot.Y != obecny_banknot.Y:
                    sprawdzone_Y = False
                # Sprawdzamy zobowiązanie bitowe dla L
                obecny_banknot.U2 = obecny_banknot.hashuj(obecny_banknot.string_S, obecny_banknot.string_B_ujawniony,
                                                          obecny_banknot.string_L_ujawniony)
                if obecny_banknot.U2 != obecny_banknot.string_U and obecny_banknot.string_S != obecny_banknot.string_S:
                    zobowiazanie_L = False
                # Sprawdzamy zobowiązanie bitowe dla R
                obecny_banknot.W2 = obecny_banknot.hashuj(obecny_banknot.string_T, obecny_banknot.string_C_ujawniony,
                                                          obecny_banknot.string_R_ujawniony)
                if obecny_banknot.W2 != obecny_banknot.string_W and obecny_banknot.string_T != obecny_banknot.string_T:
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

    def do_blind_sign(self):
        for obecny_banknot in self.banknote:
            obecny_banknot.podpis_S_zakryty = self.__klucz_prywatny.sign(obecny_banknot.Y, 0)

    def weryfikuj_podpis(self):
        weryfikacja = True
        for obecny_banknot in self.banknote:
            if not self.klucz_publiczny.verify(obecny_banknot.M_ujawniony, ((obecny_banknot.podpis_S,))):
                weryfikacja = False
        if weryfikacja:
            print "Bank zaakceptował wszystkie podpisy od sprzedawcy."
        else:
            print "Bank NIE zaakceptował podpisów banku!"

    def zdeponuj_banknot(self):
        brak_niezgodnosci = True
        for obecny_banknot in self.banknote:
            if obecny_banknot.identity_x not in self.depozyt:
                self.depozyt.append(obecny_banknot.identity_x)
                self.depozyt_S.append(obecny_banknot.S)
                if not hasattr(obecny_banknot, 'string_B_ujawniony'):
                    obecny_banknot.ujawnij_B()
                self.depozyt_B.append(obecny_banknot.string_B_ujawniony)
                if not hasattr(obecny_banknot, 'string_L_ujawniony'):
                    obecny_banknot.ujawnij_L()
                self.depozyt_L.append(obecny_banknot.string_L_ujawniony)
                self.depozyt_T.append(obecny_banknot.string_T)
                if not hasattr(obecny_banknot, 'string_C_ujawniony'):
                    obecny_banknot.ujawnij_C()
                self.depozyt_C.append(obecny_banknot.string_C_ujawniony)
                if not hasattr(obecny_banknot, 'string_R_ujawniony'):
                    obecny_banknot.ujawnij_R()
                self.depozyt_R.append(obecny_banknot.string_R_ujawniony)
            else:
                brak_niezgodnosci = False

        if brak_niezgodnosci:
            print "Bank zdeponował udanie wszystkie banknoty."
        else:
            print "Wykryto próbę podwójnego użycia banknotów!"
