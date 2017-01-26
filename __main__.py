#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tworzymy bank i Alice
from alice import Alice
from bank import Bank
from vendor import Vendor

bank = Bank()
alice = Alice()
vendor = Vendor()

# Alice przygotowuje 100 różnych banknotów Mi na ustaloną kwotę i, 0, 1, 2, …, 100
alice.generate_hundred_banknotes(100)

# Alice zakrywa wszystkie banknoty i wysyła do Banku.
alice.blind_banknotes(bank)
bank.receive_banknotes(alice.banknote)

# Alice odkrywa wybrane banknoty Mi, i != j i bank je sprawdza
bank.unblind_banknotes()

# Bank ślepo podpisuje banknote Mj i odsyła go Alice
bank.check_banknotes()
bank.do_blind_sign()

# Alice odkrywa banknoty
alice.unblind_sign(bank)

# Vendor odbiera banknoty wraz z ich podpisami
vendor.odbierz_podpisane_banknoty(alice.banknote)

# Vendor pobiera klucz publiczny banku
vendor.pobierz_klucz_publiczny(bank)

# Vendor weryfikuje podpis
vendor.weryfikuj_podpis()

# Vendor generuj 100 losowych bitów
vendor.generuj_100_bitow()

# Alice odbiera bity
alice.odbierz_bity(vendor)

# Alice w zależności od wartości bitów ujawnia zobowiazanie bitowe
vendor.sprawdz_zobowiazanie()

# Vendor wysyła banknoty do banku, który weryfikuje podpis
bank.weryfikuj_podpis()

# Bank deponuje banknoty o ile nie zostały już wcześniej użyte
bank.zdeponuj_banknot()
