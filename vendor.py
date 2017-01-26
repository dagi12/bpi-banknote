#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


class Vendor():
    def __init__(self):
        self.public_key = None
        self.bity = []

    def odbierz_signane_banknoty(self, banknot):
        self.banknot = banknot
        for current_banknote in banknot:
            current_banknote.reveal_M()

    def pobierz_public_key(self, bank):
        self.public_key = bank.public_key

    def weryfikuj_sign(self):
        weryfikacja = True
        for current_banknote in self.banknot:
            if not self.public_key.verify(current_banknote.M_revealed, ((current_banknote.sign_S,))):
                weryfikacja = False
        if weryfikacja:
            print "Vendor zaakceptował wszystkie signy Alice."
        else:
            print "Vendor NIE zaakceptował signów Alice!"

    def generuj_100_bitow(self):
        for i in range(1, 101):
            self.bity.append(random.getrandbits(1))

    def sprawdz_zobowiazanie(self):
        zobowiazanie_L = True
        zobowiazanie_R = True
        for index, current_banknote in enumerate(self.banknot):
            if self.bity[index] == 0:
                # Sprawdzamy zobowiązanie bitowe dla prawej połowy
                current_banknote.reveal_B()
                current_banknote.reveal_L()
                current_banknote.U2 = current_banknote.one_way_hash_fun(current_banknote.string_S,
                                                                        current_banknote.string_B_revealed,
                                                                        current_banknote.string_L_revealed)
                if current_banknote.U2 != current_banknote.string_U and current_banknote.string_S != current_banknote.string_S:
                    zobowiazanie_L = False

            elif self.bity[index] == 1:
                # Sprawdzamy zobowiązanie bitowe dla lewej połowy
                current_banknote.reveal_C()
                current_banknote.reveal_R()
                current_banknote.W2 = current_banknote.one_way_hash_fun(current_banknote.string_T,
                                                                        current_banknote.string_C_revealed,
                                                                        current_banknote.string_R_revealed)
                if current_banknote.W2 != current_banknote.string_W and current_banknote.string_T != current_banknote.string_T:
                    zobowiazanie_T = False

        if zobowiazanie_L:
            print "Zobowiazanie bitowe dla L zgadza się."
        else:
            print "Zobowiazanie bitowe dla L NIE zgadza się!"

        if zobowiazanie_R:
            print "Zobowiazanie bitowe dla R zgadza się."
        else:
            print "Zobowiazanie bitowe dla R NIE zgadza się!"
