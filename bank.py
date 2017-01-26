#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Crypto.PublicKey import RSA


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

    def odbierz_banknoty(self, banknot):
        self.banknot = banknot

    def odkryj_banknoty(self):
        self.wyklucz = random.randint(0, 99)
        for index, obecny_banknot in enumerate(self.banknot):
            if index != self.wyklucz:
                obecny_banknot.ujawnij_B()
                obecny_banknot.ujawnij_L()
                obecny_banknot.ujawnij_Z()
                obecny_banknot.ujawnij_C()
                obecny_banknot.ujawnij_R()
                obecny_banknot.M_odkryte = self.klucz_publiczny.unblind(obecny_banknot.Y[0],
                                                                        obecny_banknot.ciag_Z_ujawniony)

    def sprawdz_banknoty(self):
        identyfikatory = []
        rozne_identyfikatory = True
        sprawdzone_Y = True
        zobowiazanie_L = True
        zobowiazanie_R = True

        for index, obecny_banknot in enumerate(self.banknot):
            if index != self.wyklucz:
                # Sprawdzamy czy identyfikatory są różne
                if obecny_banknot.identyfikator in identyfikatory:
                    rozne_identyfikatory = False
                else:
                    identyfikatory.append(obecny_banknot.identyfikator)
                # Sprawdzamy czy Y są takie same
                if obecny_banknot.Y != obecny_banknot.Y:
                    sprawdzone_Y = False
                # Sprawdzamy zobowiązanie bitowe dla L
                obecny_banknot.U2 = obecny_banknot.hashuj(obecny_banknot.ciag_S, obecny_banknot.ciag_B_ujawniony,
                                                          obecny_banknot.ciag_L_ujawniony)
                if obecny_banknot.U2 != obecny_banknot.ciag_U and obecny_banknot.ciag_S != obecny_banknot.ciag_S:
                    zobowiazanie_L = False
                # Sprawdzamy zobowiązanie bitowe dla R
                obecny_banknot.W2 = obecny_banknot.hashuj(obecny_banknot.ciag_T, obecny_banknot.ciag_C_ujawniony,
                                                          obecny_banknot.ciag_R_ujawniony)
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
