from models import Sklep, Kategoria, Produkt

def create_test_shop():

    sklep = Sklep(
        nazwa="Python Shop",
        stan_konta=0
    )

    magazyn = sklep.magazyn

    # Kategorie
    nabial = Kategoria("Nabiał")
    pieczywo = Kategoria("Pieczywo")
    napoje = Kategoria("Napoje")
    warzywa = Kategoria("Warzywa")
    slodycze = Kategoria("Słodycze")

    for kat in (
        nabial,
        pieczywo,
        napoje,
        warzywa,
        slodycze
    ):
        magazyn.dodaj_kategorie(kat)

    # Produkty
    produkty = [
        Produkt("Mleko 3.2%", 4.99, 120, nabial),
        Produkt("Masło ekstra", 8.99, 50, nabial),
        Produkt("Jogurt naturalny", 2.99, 75, nabial),
        Produkt("Chleb wiejski", 5.49, 40, pieczywo),
        Produkt("Bułka kajzerka", 0.79, 200, pieczywo),
        Produkt("Woda mineralna", 2.49, 150, napoje),
        Produkt("Sok pomarańczowy", 6.99, 35, napoje),
        Produkt("Pomidor", 12.99, 25, warzywa),
        Produkt("Ogórek", 8.99, 30, warzywa),
        Produkt("Czekolada mleczna", 4.49, 80, slodycze),
    ]

    for produkt in produkty:
        magazyn.dodaj_produkt(produkt)

    return sklep

def create_test_client():
    return Klient("Jan Kowalski")