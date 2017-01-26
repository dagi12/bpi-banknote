# bpi-banknote

pip2 install pycrypto

Tworzenie Banknotu
Alice przygotowuje 100 bankntów Mi
Mi posiada Ustaloną kwotę Y
Losowy identifkator banknotu Xi [1,100],

liczba bitów powinna być odpowiednio duża by nie powtórzyć 100 różnych zestawów ciągów identyfikujących Alice
Protokół rozdzielenia tajemnicę Ii, j dla dwóch stron (yi, 1, …, 100)
W ten sposób otrzymujemy 2 ciągi bitów Lij, Rij
Którego XOR daje Ii,j
Zobowiązanie bitowe dla Li,j i Ri,j Tu używamy zobowiązania bitowego za pomocą jednokierunkowej f. Hashującej H
M1 = [y][x1][s1,1, U1,1, s1,100, U1,100][T1,1, W1,1, T1, 100, W1,100]
Protokół rozdzielenia tajemnicy Ii,j
Alice losuje ciąg Ri,j
Alice oblicza Li,j = Ii,j XOR Rij
W ten sposób Alice wyznacza ciągi Li,j i Ri,j

Protokół Zobowiązania bitowego
Dla Ri,j za pomocą jednokierunkwej f. Hashującej H
Alice losuje 2 ciągi Ti,j i Ci,j. Liczba bitów powinna uniemożliwić znalezienie konfliktu dla H
Alice oblicza H(Ti,j, Ci,j, Ri,j) = Wi,j
Alice umieszcza ciągi wyżej napisane w banknocie a ciąg Ci,j zachowuje w sekrecie
Dla Li,j za pomocą jednokierunkowej f. Hashującej H
Alice losuje 2 ciągi Si,j i Bi,j Liczba bitów powinna uniemożliwiać znalezienie konfliktu dla H
Alice oblicza H(Si,j, Bi,j,Li,j) = Ui,j
Alice umieszcza ciągi Sij, Uij w banknocie a ciąg Bij zachowuje w sekrecie
Przesyłanie banknotu
Teraz Alice chce uzyskać ślepy podpis pod jednym z banknotów Mi. Wtedy Alice będzie miała 1 ważny banknot, za który sprzedawca otrzyma określoną na nim kwotę. Co więcej, zakup będzie anonimowy, bo bank nie będzie znał identyfikatora banknotu, ani danych identyfikacyjnych Alice. Bank natomiast musi ze swojej strony być pewny, że banknot Mi jest utworzony zgodnie z protokołem. Ważna dla bnaku jest czy kwota Y się zgadza. Stosowana wtedy przez bank technika dziel i wybieraj. Wtedy bank przekona się co do poprawności konstrukcji banknotów i wykryje ewentualne oszustwo Alice

Alice pobiera klucz publiczny banku K dla ślepego podpisu
Alice zakrywa banknoty jak do ślepego podpisu RSA
Alice wysyła 100 zakrytych bankotów do banku
Bank losowo wybiera liczbę j z [1,100] i żąda odkrycia wszystkich bankotów poza wybranym oraz ujawnienia zobowiązań bitowych zawartych w nich.
Alice wykonuje polecenia banku
Bank odkrywa wszystkie banknoty poza wybranym
K = [EN] – public, k = [D,N] = private



W celu zakrycia banknotu Mi jak do ślepego podpisu RSA, Alice robi tak:
Alice pobiera K = [E,N] do ślepego podpisu
Alice losuje Zi takie, że (Zi, N) = 1
Alice oblicza Yi = MiZiE ( mod N)
Alice wysyła Yi do banku
W wcelu odkrycia przez bank wszystkich banknotów poza Yj wykonywane są
Alice wysyła do banku ciągi Zi [1,100]
Bank oblicza Mi = YiZi-E (mod N) dla i != j
Sprawdzanie banknotu
Teraz bank sprawdzi czy banknoty Alice zostały utworzone zgodnie z protoołem. Jeśli nie – przerywa protokół i donosi na policję o próbie dokonania przestępstwa przez Alice.
Po skontrolowaniu przez bank jest w 100%(99%) pewny zgodności Alice na 1/100 szansę na oszukanie banku

Bank sprawda czy wszystkie Mi, i != j zawierają identyczną wartość Y – kwotę
Bank sprawdza czy wszystkie Mi zawierają różne identyifaktory Xi
Bank weryfikuje zobowiązanie bitowe Li,k, gdzie i != j, k = [1,100]
Bank oblicza H(Si,k, Bi,k, Li,k) = Ui,k
Bank sprawdza czy U’i,k jest identyczne z Ui,k z bankotu Mi, jeśli nie – przerywa protokół
Ban ksprawdza czy Si,k przesłane przez Alice jest identyczne z Si,k z banknotu Mi, jeśli nie przerywa
Bank weryfikuje zobowiązanie bitowe Ri,k
Bank oblicza H(Ti,k, Ci,k, Ri,k) z W’i,k
Sprawdza identyczność W’i,k z Wi,k z bankotu Mi
Sprawdza identyczność T’i,k z Ti,k z banknotu Mi
Bank oblicza Ii,k = Li,k XOR Ri,k
Bank sprawdza czy wszystkie Ii,k identyfikują Alice
Wydanie Banknotu
Bank ślepo podpisuje swoim kluczem tajnym k zakrytą wiadomość Mj i odsyła do Alice. Alice odkrywa Mj banknot i ma nad nim ważny podpis banku
	Yj – zakryty banknot Mj k = [D,N] – klucz tajny Alice do ślepego Podpisu

Bank:
Bank oblicza vj = YjD(mod N)
Bank wysyła Vj do Alice
Vj – jślepy podpis RSA pod Yj, Zj – wartość, którą Alice wybrała do zakrycia Mj do ślepego podpisu RSA
Alice chce odkryć Mj
Alice oblicza Sj = VjZj-1 mod N
Teraz Alice ma banknot Mj ze ślepym podpisem Sj pod Mj. Posiada ciągi Zj oraz Bj,i, Lj,i, Cj,i, Rj,i ściśle związane z Mj



ODPORNOŚĆ NA OSZUSTWA

Alice wykorzystuje banknot dwukrotnie
Alice chce zapłacić Bobowi a potem Dave’owi. Bob przekazuje Alice losowy ciąg biów b [1,100], a Alice na tej upodstawie:
Ujawnia Lj, s  lewej połowy identyfikujących ją bitów
Ujawnia Rj,t prawej połowy identyfikujących ją bitów
Dave przekazuje C1…C100 a Alice ujawnia Lj,u i Rj,u, v, w, u != w
Bob i Dave przekazują do banku Lj,s Rj,s i Lj,u Rj,u od Alice to z dużym prawdopodobieństwem istnieje k takie że bk = ck. Bank może znaleźć parę Lj,k i Rj,l na podstawie którego oblicza Ij,k = Lj,k XOR Rj,k. Z Założenia protokołu widać, że Ij,k identyfikuje Alicce czyli ujawnia oszusta.

Sprzedawca wykorzystujebanknot dwukrotnie
W czasie 1-szego deponowania banknotu w banku ujawnia Lj,s i Rj,t lewe i prawe połowy ciągów, które identyifukują Alice
W czasie 2-giego deponowania:
Sprzedawca dostarcza Mj z Sj ale nie może ich zmienić bo jest podpisane przez bank
Bank dostaje identyczne banknoty i ciągi identyfikujące Alice, a otrzymwanie dwóch identycznych zestawów ciągów identyfikujących Alice jest prawie niemożliwe
Anonimowość transakcji
Jeżeli Alice nie oszukuje to bank nie ma możliwości wykrycia od kogo sprzedawca otrzymał Mj