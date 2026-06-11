# Modele pod obsługę sklepu

class Kategoria:
    def __init__(self, kategoria_id:int, nazwa:str):
        self.kategoria_id = kategoria_id
        self.nazwa = nazwa

    def __str__(self):
        return f"{self.kategoria_id}: {self.nazwa}"


class Produkt:
    def __init__(self, produkt_id:int, nazwa:str, cena:float, stan_magazynowy:int, kategoria:Kategoria | None = None):
        if kategoria is not None and not isinstance(kategoria, Kategoria):
            raise TypeError("Kategoria musi być obiektem klasy Kategoria")

        self.produkt_id = produkt_id
        self.nazwa = nazwa
        self.cena = cena
        self.stan_magazynowy = stan_magazynowy
        self.kategoria = kategoria

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

        # Domyślna kategoria na produkty
        self.kategorie[0] = Kategoria(
            kategoria_id=0,
            nazwa="Uncategorised"
        )

    # Produkty
    def dodaj_produkt(self, produkt: Produkt):
        if produkt.kategoria is None:
            produkt.kategoria = self.kategorie[0]

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

    def pobierz_produkt(self, produkt_id: int):
        if produkt_id not in self.produkty:
            raise KeyError("Brak produktu w magazynie")
        else:
            return self.produkty[produkt_id]

    def wyswietl_produkty(self):
        for produkt in self.produkty.values():
            print(f"Produkt ID: {produkt.produkt_id}")
            print(produkt)
            print("-"*40)

    # Kategorie
    def dodaj_kategorie(self, kategoria: Kategoria):
        if kategoria.kategoria_id in self.kategorie:
            pass
        else:
            self.kategorie[kategoria.kategoria_id] = kategoria

    def usun_kategorie(self, kategoria_id: int):
        if kategoria_id == 0:
            raise ValueError("Nie można usunąć kategorii domyślnej")

        if kategoria_id in self.kategorie:
            for produkt in self.produkty.values():
                if produkt.kategoria == self.kategorie[kategoria_id]:
                    produkt.kategoria = self.kategorie[0]

            del self.kategorie[kategoria_id]
        else:
            raise KeyError(f"W magazynie brak kategorii o numerze ID: {kategoria_id}")

    def pobierz_kategorie(self, kategoria_id: int):
        if kategoria_id not in self.kategorie:
            raise KeyError("Brak kategorii w magazynie")
        else:
            return self.kategorie[kategoria_id]

    def wyswietl_kategorie(self):
        for kategoria in self.kategorie.values():
            print(kategoria)


    # Magazyn
    def wyswietl_stan(self):
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


class Zamowienie:
    pass


class Platnosc:
    pass


class Konto:
    pass


class Klient:
    pass


class Sklep:
    pass