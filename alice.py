#!/usr/bin/env python
# -*- coding: utf-8 -*-
from banknote import Banknote


# Alica – klientka banku i chce otrzymać elektroniczny banknote, którym będzie mogła dokonać zakupu w dowolnym sklepie.
#  Transakcja Alice będzie anonimowa jeżeli ona będzie postępować zgodnie z protokołem
# I wydanie elektronicznego banknotu przez bank
class Alice():
    def __init__(self):
        self.banknote = []
        self.M = None

    def generate_hundred_banknotes(self, amountY):
        for i in range(1, 101):
            self.banknote.append(Banknote(amountY))

    def blind_banknotes(self, bank):
        for current_banknote in self.banknote:
            current_banknote.blind_banknote(bank)

    def unblind_sign(self, bank):
        for current_banknote in self.banknote:
            current_banknote.ujawnij_Z()
            current_banknote.podpis_S = bank.klucz_publiczny.unblind(current_banknote.podpis_S_zakryty[0],
                                                                     current_banknote.string_Z_ujawniony)

    def odbierz_bity(self, sprzedawca):
        self.bity = sprzedawca.bity
