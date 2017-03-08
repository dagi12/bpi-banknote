#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

from Crypto.PublicKey import RSA


class Bank():
    def __init__(self):
        self.__private_key = RSA.generate(2048)
        self.public_key = self.__private_key.publickey()
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
        # Bank losowo wybiera liczbę j z [1,100]
        self.exclude = random.randint(0, 99)
        # i żąda odkrycia wszystkich bankotów poza wybranym
        for index, current_banknote in enumerate(self.banknote):
            if index != self.exclude:
                # oraz ujawnienia zobowiązań bitowych zawartych w nich.
                current_banknote.reveal_B()
                current_banknote.reveal_L()
                current_banknote.reveal_Z()
                current_banknote.reveal_C()
                current_banknote.reveal_R()
                # W wcelu odkrycia przez bank wszystkich banknotów poza Yj wykonywane są
                # Alice wysyła do banku ciągi Zi [1,100]
                # Bank oblicza Mi = YiZi-E (mod N) dla i != j
                current_banknote.M_odkryte = self.public_key.unblind(current_banknote.Y[0],
                                                                     current_banknote.string_Z_revealed)

    def check_banknotes(self):
        identities = []
        different_identities = True
        checked_Y = True
        l_commitment = True
        r_commitment = True

        for index, current_banknote in enumerate(self.banknote):
            if index != self.exclude:

                # Bank sprawda czy wszystkie Mi, i != j zawierają identyczną wartość Y – kwotę
                if current_banknote.Y != current_banknote.Y:
                    checked_Y = False

                # Sprawdzamy zobowiązanie bitowe dla L
                # Bank oblicza H(Si,k, Bi,k, Li,k) = Ui,k
                current_banknote.U2 = current_banknote.one_way_hash_fun(current_banknote.string_S,
                                                                        current_banknote.string_B_revealed,
                                                                        current_banknote.string_L_revealed)
                if current_banknote.U2 != current_banknote.string_U and current_banknote.string_S != current_banknote.string_S:
                    l_commitment = False

                # Sprawdzamy zobowiązanie bitowe dla R
                current_banknote.W2 = current_banknote.one_way_hash_fun(current_banknote.string_T,
                                                                        current_banknote.string_C_revealed,
                                                                        current_banknote.string_R_revealed)
                if current_banknote.W2 != current_banknote.string_W and current_banknote.string_T != current_banknote.string_T:
                    zobowiazanie_T = False

                # Bank sprawdza czy wszystkie Ii,k identyfikują Alice
                if current_banknote.identity_x in identities:
                    different_identities = False
                else:
                    identities.append(current_banknote.identity_x)

        if different_identities:
            print "Wszystkie identities różnią się od siebie."
        else:
            print "Identyczne identities w banknotach!"

        if checked_Y:
            print "Wszystkie banknoty mają identyczną zawartość Y."
        else:
            print "Zawartość Y w banknotach nie zgadza się!"

        if l_commitment:
            print "Zobowiazanie bitowe dla L zgadza się."
        else:
            print "Zobowiazanie bitowe dla L NIE zgadza się!"

        if r_commitment:
            print "Zobowiazanie bitowe dla R zgadza się."
        else:
            print "Zobowiazanie bitowe dla R NIE zgadza się!"

    def do_blind_sign(self):
        current_banknote = self.banknote[self.exclude]
        current_banknote.sign_S_blinded = self.__private_key.sign(current_banknote.Y, 0)
        return current_banknote

    def weryfikuj_sign(self):
        weryfikacja = True
        for current_banknote in self.banknote:
            if not self.public_key.verify(current_banknote.M_revealed, ((current_banknote.sign_S,))):
                weryfikacja = False
        if weryfikacja:
            print "Bank zaakceptował wszystkie signy od sprzedawcy."
        else:
            print "Bank NIE zaakceptował signów banku!"

    def zdeponuj_banknot(self):
        brak_niezgodnosci = True
        for current_banknote in self.banknote:
            if current_banknote.identity_x not in self.depozyt:
                self.depozyt.append(current_banknote.identity_x)
                self.depozyt_S.append(current_banknote.S)
                if not hasattr(current_banknote, 'string_B_revealed'):
                    current_banknote.reveal_B()
                self.depozyt_B.append(current_banknote.string_B_revealed)
                if not hasattr(current_banknote, 'string_L_revealed'):
                    current_banknote.reveal_L()
                self.depozyt_L.append(current_banknote.string_L_revealed)
                self.depozyt_T.append(current_banknote.string_T)
                if not hasattr(current_banknote, 'string_C_revealed'):
                    current_banknote.reveal_C()
                self.depozyt_C.append(current_banknote.string_C_revealed)
                if not hasattr(current_banknote, 'string_R_revealed'):
                    current_banknote.reveal_R()
                self.depozyt_R.append(current_banknote.string_R_revealed)
            else:
                brak_niezgodnosci = False

        if brak_niezgodnosci:
            print "Bank zdeponował udanie wszystkie banknoty."
        else:
            print "Wykryto próbę podwójnego użycia banknotów!"
