# Modele pod obsługę sklepu

class Kategoria:
    def __init__(self, kategoria_id:int, nazwa:str):
        self.kategoria_id = kategoria_id
        self.nazwa = nazwa

    def __str__(self):
        return f"{self.kategoria_id}: {self.nazwa}"


class Produkt:
    def __init__(self, produkt_id:int, nazwa:str, cena:float, stan_magazynowy:int, kategoria:Kategoria):
        if not isinstance(kategoria, Kategoria):
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

    @property
    def dostepny(self) -> bool:
        return self.stan_magazynowy > 0

    def __str__(self):
        return (
            f"{self.nazwa}\n"
            f"\tCena: {self.cena:.2f} zł\n"
            f"\tStan: {self.stan_magazynowy}\n"
            f"\tKategoria: {self.kategoria.nazwa}"
        )

    def __repr__(self):
        return f"Produkt (id={self.produkt_id}, nazwa='{self.nazwa}')"


class Magazyn:
    def __init__(self):
        self.produkty = {}


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