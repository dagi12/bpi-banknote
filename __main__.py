#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Tworzymy bank i Alice
from alice import Alice
from bank import Bank
from vendor import Sprzedawca

bank = Bank()
alice = Alice()
sprzedawca = Sprzedawca()

# Alice tworzy 100 banknotów
alice.generuj_100_banknotow(100)

# Alice zakrywa banknoty
alice.zakryj_banknoty(bank)

# Alice wysyła wszystkie 100 banknotów ZAKRYTYCH do banku
bank.odbierz_banknoty(alice.banknot)

# Alice ujawnia 99 banknotów poza j-tym
bank.odkryj_banknoty()

# Bank sprawdza 99 banknotów
bank.sprawdz_banknoty()

# Bank ślepo podpisuje wszystkie banknoty
bank.zloz_slepy_podpis()

# Alice odkrywa banknoty
alice.odkryj_podpis(bank)

# Sprzedawca odbiera banknoty wraz z ich podpisami
sprzedawca.odbierz_podpisane_banknoty(alice.banknot)

# Sprzedawca pobiera klucz publiczny banku
sprzedawca.pobierz_klucz_publiczny(bank)

# Sprzedawca weryfikuje podpis
sprzedawca.weryfikuj_podpis()

# Sprzedawca generuj 100 losowych bitów
sprzedawca.generuj_100_bitow()

# Alice odbiera bity
alice.odbierz_bity(sprzedawca)

# Alice w zależności od wartości bitów ujawnia zobowiazanie bitowe
sprzedawca.sprawdz_zobowiazanie()

# Sprzedawca wysyła banknoty do banku, który weryfikuje podpis
bank.weryfikuj_podpis()

# Bank deponuje banknoty o ile nie zostały już wcześniej użyte
bank.zdeponuj_banknot()
