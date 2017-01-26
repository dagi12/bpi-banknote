#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


class Sprzedawca():
    def __init__(self):
        self.klucz_publiczny = None
        self.bity = []

    def odbierz_podpisane_banknoty(self, banknot):
        self.banknot = banknot
        for obecny_banknot in banknot:
            obecny_banknot.ujawnij_M()

    def pobierz_klucz_publiczny(self, bank):
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
        for i in range(1, 101):
            self.bity.append(random.getrandbits(1))

    def sprawdz_zobowiazanie(self):
        zobowiazanie_L = True
        zobowiazanie_R = True
        for index, obecny_banknot in enumerate(self.banknot):
            if self.bity[index] == 0:
                # Sprawdzamy zobowiązanie bitowe dla prawej połowy
                obecny_banknot.ujawnij_B()
                obecny_banknot.ujawnij_L()
                obecny_banknot.U2 = obecny_banknot.hashuj(obecny_banknot.ciag_S, obecny_banknot.ciag_B_ujawniony,
                                                          obecny_banknot.ciag_L_ujawniony)
                if obecny_banknot.U2 != obecny_banknot.ciag_U and obecny_banknot.ciag_S != obecny_banknot.ciag_S:
                    zobowiazanie_L = False

            elif self.bity[index] == 1:
                # Sprawdzamy zobowiązanie bitowe dla lewej połowy
                obecny_banknot.ujawnij_C()
                obecny_banknot.ujawnij_R()
                obecny_banknot.W2 = obecny_banknot.hashuj(obecny_banknot.ciag_T, obecny_banknot.ciag_C_ujawniony,
                                                          obecny_banknot.ciag_R_ujawniony)
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
