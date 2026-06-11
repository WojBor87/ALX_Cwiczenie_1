# Modele pod obsługę sklepu

class Kategoria:
    next_id = 0

    def __init__(self,nazwa:str):
        self.nazwa = nazwa
        self.kategoria_id = Kategoria.next_id
        Kategoria.next_id += 1

    def __str__(self):
        return f"{self.kategoria_id}: {self.nazwa}"


class Produkt:
    next_id = 0

    def __init__(self, nazwa:str, cena:float, stan_magazynowy:int, kategoria:Kategoria | None = None):
        if kategoria is not None and not isinstance(kategoria, Kategoria):
            raise TypeError("Kategoria musi być obiektem klasy Kategoria")

        self.produkt_id = Produkt.next_id
        self.nazwa = nazwa
        self.cena = cena
        self.stan_magazynowy = stan_magazynowy
        self.kategoria = kategoria

        Produkt.next_id += 1

    # Walidacja wartości
    @property
    def cena(self) -> float:
        return self._cena

    @cena.setter
    def cena(self, price:float):
        if not isinstance(price, (int, float)):
            raise TypeError("Cena musi być liczbą")

        if price <= 0:
            raise ValueError("Cena musi być większa od 0")

        self._cena = float(price)

    @property
    def stan_magazynowy(self) -> int:
        return self._stan_magazynowy

    @stan_magazynowy.setter
    def stan_magazynowy(self, amount:int):
        if not isinstance(amount, int):
            raise TypeError("Stan magazynowy musi być liczbą całkowitą")

        if amount < 0:
            raise ValueError("Stan magazynowy nie może być ujemny")

        self._stan_magazynowy = amount

    # metody klasy
    def zmien_cene(self, nowa_cena: float) -> None:
        self.cena = nowa_cena

    def dostawa(self, liczba_sztuk:int) -> None:
        if not isinstance(liczba_sztuk, int):
            raise TypeError("Liczba sztuk musi być liczbą całkowitą")

        if liczba_sztuk <= 0:
            raise ValueError("Liczba sztuk musi być większa od zera")

        self.stan_magazynowy += liczba_sztuk

    def sprzedaz(self, liczba_sztuk:int) -> None:
        if not isinstance(liczba_sztuk, int):
            raise TypeError("Liczba sztuk musi być liczbą całkowitą")

        if liczba_sztuk <= 0:
            raise ValueError("Liczba sztuk musi być dodatnia")

        if liczba_sztuk > self.stan_magazynowy:
            raise ValueError("Brak wystarczającej ilości towaru")

        self.stan_magazynowy -= liczba_sztuk

    # Właściwości
    @property
    def dostepny(self) -> bool:
        return self.stan_magazynowy > 0

    # Wyświetlanie
    def __str__(self):
        return (
            f"{self.nazwa}\n"
            f"\tCena: \t{self.cena:.2f} zł\n"
            f"\tStan: \t{self.stan_magazynowy}\n"
            f"\tKategoria: \t{self.kategoria.nazwa if self.kategoria else 'Uncategorised'}"
        )

    def __repr__(self):
        return f"Produkt (id={self.produkt_id}, nazwa='{self.nazwa}')"


class Magazyn:
    def __init__(self, name:str):
        self.name = name
        self.produkty = {}
        self.kategorie = {}

        self.domyslna_kategoria = Kategoria("Uncategorised")

        self.kategorie[
            self.domyslna_kategoria.kategoria_id
        ] = self.domyslna_kategoria

    # Produkty
    def dodaj_produkt(self, produkt: Produkt) -> None:
        if produkt.kategoria is None:
            produkt.kategoria = self.domyslna_kategoria

        if produkt.produkt_id in self.produkty:
            istniejacy = self.produkty[produkt.produkt_id]

            istniejacy.dostawa(produkt.stan_magazynowy)
        else:
            self.produkty[produkt.produkt_id] = produkt

    def usun_produkt(self, produkt_id: int):
        if produkt_id in self.produkty:
            del self.produkty[produkt_id]
        else:
            raise KeyError(f"W magazynie brak produktu o numerze ID: {produkt_id}")

    def pobierz_produkt(self, produkt_id: int) -> Produkt:
        if produkt_id not in self.produkty:
            raise KeyError("Brak produktu w magazynie")
        return self.produkty[produkt_id]

    def wyswietl_produkty(self):
        if not self.produkty:
            print("Brak produktów")
            return

        for produkt in self.produkty.values():
            print(f"Produkt ID: {produkt.produkt_id}")
            print(produkt)
            print("-"*40)

    # Kategorie
    def dodaj_kategorie(self, kategoria: Kategoria) -> None:
        if kategoria.kategoria_id in self.kategorie:
            raise ValueError("Kategoria już istnieje")
        self.kategorie[kategoria.kategoria_id] = kategoria

    def usun_kategorie(self, kategoria_id: int):
        if kategoria_id == self.domyslna_kategoria.kategoria_id:
            raise ValueError("Nie można usunąć kategorii domyślnej")

        if kategoria_id in self.kategorie:
            for produkt in self.produkty.values():
                if produkt.kategoria == self.kategorie[kategoria_id]:
                    produkt.kategoria = self.domyslna_kategoria

            del self.kategorie[kategoria_id]
        else:
            raise KeyError(f"W magazynie brak kategorii o numerze ID: {kategoria_id}")

    def pobierz_kategorie(self, kategoria_id: int) -> Kategoria:
        if kategoria_id not in self.kategorie:
            raise KeyError("Brak kategorii w magazynie")
        return self.kategorie[kategoria_id]

    def wyswietl_kategorie(self):
        for kategoria in self.kategorie.values():
            print(kategoria)


    # Magazyn
    def wyswietl_stan(self):
        if not self.produkty:
            print("Magazyn jest pusty")
            return

        for produkt in self.produkty.values():
            print(f"{produkt.nazwa}: {produkt.stan_magazynowy}")

    def czy_istnieje(self, produkt_id: int) -> bool:
        return produkt_id in self.produkty

    # Wyświetlanie
    def __str__(self):
        return (
            f"{self.name}\n"
            f"Produkty w magazynie: {len(self.produkty)}\n"
            f"Kategorii produktów w magazynie: {len(self.kategorie)}"
        )

    def __repr__(self):
        return f"Magazyn (name={self.name})"


class Koszyk:
    def __init__(self):
        self.pozycje = {}

    def dodaj(self, produkt:Produkt, liczba_szt:int) -> None:
        if liczba_szt <= 0:
            raise ValueError("Nie można dodać niedodatniej liczby sztuk")
        if liczba_szt > produkt.stan_magazynowy:
            raise ValueError(f"Brak wystarczającej liczby sztuk w magazynie. Dostępna liczba: {produkt.stan_magazynowy}")

        aktualnie_w_koszyku = 0

        if produkt.produkt_id in self.pozycje:
            aktualnie_w_koszyku = self.pozycje[produkt.produkt_id]["ilosc"]

        if aktualnie_w_koszyku + liczba_szt > produkt.stan_magazynowy:
            raise ValueError("Sumarycznie dodana liczba sztuk przekracza stan_magazynowy")

        if produkt.produkt_id in self.pozycje:
            self.pozycje[produkt.produkt_id]["ilosc"] += liczba_szt
        else:
            self.pozycje[produkt.produkt_id] = {
                "produkt": produkt,
                "ilosc": liczba_szt,
            }

    def usun(self, produkt_id: int, liczba_szt:int | None=None) -> None:
        if produkt_id not in self.pozycje:
            raise KeyError("Nie ma takiego produktu w koszyku")
        if liczba_szt is None:
            del self.pozycje[produkt_id]
            return

        if not isinstance(liczba_szt, int):
            raise TypeError("Liczba sztuk musi być liczbą całkowitą")

        if liczba_szt <= 0:
            raise ValueError("Liczba sztuk musi być dodatnia")

        aktualna_ilosc = self.pozycje[produkt_id]["ilosc"]

        if liczba_szt >= aktualna_ilosc:
            del self.pozycje[produkt_id]
        else:
            self.pozycje[produkt_id]["ilosc"] -= liczba_szt

    def wartosc_koszyka(self) -> float:
        suma = 0
        for pozycja in self.pozycje.values():
            produkt = pozycja["produkt"]
            ilosc = pozycja["ilosc"]
            suma += produkt.cena * ilosc
        return suma

    @property
    def pusty(self) -> bool:
        return len(self.pozycje) == 0

    def wyswietl(self):
        if self.pusty:
            print("Koszyk jest pusty.")
            return

        print("\nZawartość koszyka:")
        for pozycja in self.pozycje.values():
            produkt = pozycja["produkt"]
            ilosc = pozycja["ilosc"]
            print(f"{produkt.nazwa} x {ilosc} = {produkt.cena * ilosc:.2f} zł")

        print(f"Razem: {self.wartosc_koszyka():.2f} zł")

    def __str__(self):
        if self.pusty:
            return "Koszyk jest pusty"

        return (
            f"Liczba produktów: {len(self.pozycje)}\n"
            f"Wartość koszyka: {self.wartosc_koszyka():.2f} zł"
        )

    def __repr__(self):
        return f"Koszyk(pozycje={len(self.pozycje)})"


class Klient:
    def __init__(self, imie:str):
        self.imie = imie
        self.koszyk = Koszyk()

    def __str__(self):
        return f"Klient: {self.imie}"

    def __repr__(self):
        return f"Klient(imie='{self.imie}')"


class Zamowienie:
    def __init__(self, klient: Klient):
        self.klient = klient
        self.wartosc_zamowienia = self.wartosc

    @property
    def wartosc(self):
        return self.klient.koszyk.wartosc_koszyka()

    def zamow(self) -> float:
        if self.klient.koszyk.pusty:
            raise ValueError("Koszyk jest pusty")

        # Jeżeli w między czasie inny klient kupił produkty z koszyka, musimy mieć drugą walidacje
        # ilości sztuk dostępnychw magazynie

        for pozycja in self.klient.koszyk.pozycje.values():
            produkt = pozycja["produkt"]
            ilosc = pozycja["ilosc"]

            if ilosc > produkt.stan_magazynowy:
                raise ValueError(f"Produkt {produkt.nazwa} jest już niedostępny w wymaganej ilosci")

        for pozycja in self.klient.koszyk.pozycje.values():
            produkt = pozycja["produkt"]
            ilosc = pozycja["ilosc"]

            produkt.sprzedaz(ilosc)

        self.klient.koszyk.pozycje.clear()

        return self.wartosc_zamowienia

class Platnosc:
    def __init__(self, kwota: float):
        self.kwota = kwota

    def wykonaj(self, sklep: Sklep):
        sklep.stan_konta += self.kwota


class Sklep:
    def __init__(self, nazwa:str, stan_konta:float):
        self.nazwa = nazwa
        self.magazyn = Magazyn(nazwa)
        self.stan_konta = stan_konta

    @property
    def stan_konta(self) -> float:
        return self._stan_konta

    @stan_konta.setter
    def stan_konta(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeError("Stan konta musi być liczbą")

        if value < 0:
            raise ValueError("Stan konta nie może być ujemny")

        self._stan_konta = float(value)
