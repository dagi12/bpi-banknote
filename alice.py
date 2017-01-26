#!/usr/bin/env python
# -*- coding: utf-8 -*-
from banknote import Banknot


class Alice():
    def __init__(self):
        self.banknot = []
        self.M = None

    def generuj_100_banknotow(self, kwota):
        for i in range(1, 101):
            self.banknot.append(Banknot(kwota))

    def zakryj_banknoty(self, bank):
        for obecny_banknot in self.banknot:
            obecny_banknot.zakryj_banknot(bank)

    def odkryj_podpis(self, bank):
        for obecny_banknot in self.banknot:
            obecny_banknot.ujawnij_Z()
            obecny_banknot.podpis_S = bank.klucz_publiczny.unblind(obecny_banknot.podpis_S_zakryty[0],
                                                                   obecny_banknot.ciag_Z_ujawniony)

    def odbierz_bity(self, sprzedawca):
        self.bity = sprzedawca.bity
