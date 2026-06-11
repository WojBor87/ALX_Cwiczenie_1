from seed import create_test_warehouse
from models import Produkt, Kategoria, Magazyn

magazyn = create_test_warehouse()
konto = create_test_account()

magazyn.wyswietl_stan()

magazyn.wyswietl_produkty()

magazyn.wyswietl_kategorie()

jablko = Produkt("jabłko", 2.20, 40)
magazyn.dodaj_produkt(jablko)

for produkt in magazyn.produkty.values():
    if produkt.kategoria == magazyn.kategorie[0]:
        print(produkt)

