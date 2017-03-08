#!/usr/bin/env python
# -*- coding: utf-8 -*-
from banknote import Banknote


# Alica – klientka banku i chce otrzymać elektroniczny banknote, którym będzie mogła dokonać zakupu w dowolnym sklepie.
#  Transakcja Alice będzie anonimowa jeżeli ona będzie postępować zgodnie z protokołem
# I wydanie elektronicznego banknotu przez bank
class Alice:
    def __init__(self):
        self.banknote = []

    def generate_hundred_banknotes(self, amount_y):
        for i in range(1, 101):
            self.banknote.append(Banknote(amount_y))

    def blind_banknotes(self, public_key):
        for current_banknote in self.banknote:
            current_banknote.blind_banknote(public_key)

    def unblind_sign(self, banknote_j, bank):
        banknote_j.reveal_Z()
        banknote_j.sign_S = bank.public_key.unblind(banknote_j.sign_S_blinded[0],
                                                    banknote_j.string_Z_revealed)
