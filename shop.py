from seed import create_test_shop, create_test_client

def menu(nazwa):
    print(f"\n=== {nazwa} ===")
    print("1. Wyświetl dostępne produkty")
    print("2. Dodaj produkt do koszyka")
    print("3. Pokaż koszyk")
    print("4. Usuń produkt z koszyka")
    print("5. Złóż zamówienie")
    print("6. Pokaż stan konta sklepu")
    print("7. Magazyn")
    print("0. Wyjście")

def menu_magazyn():
    print("\n=== MAGAZYN ===")
    print("1. Pokaż kategorie")
    print("2. Pokaż wszystkie produkty")
    print("3. Pokaż produkty z kategorii")
    print("0. Powrót")


def main():
    sklep = create_test_shop()
    klient = create_test_client()

    while True:
        menu(sklep.nazwa)

        poprawny_wybor = False
        while not poprawny_wybor:
            wybor = input("Wybierz opcję: ")
            if wybor.isdigit():
                poprawny_wybor = True
            else:
                print("Wskaż numer pozycji z menu aplikacji")

        if wybor == "1":
            sklep.magazyn.wyswietl_produkty()

        elif wybor == "2":
            produkt_id = int(input("ID produktu: "))
            ilosc = int(input("Liczba sztuk: "))

            produkt = sklep.magazyn.pobierz_produkt(produkt_id)

            klient.koszyk.dodaj(produkt, ilosc)

            print("Produkt dodany do koszyka.")

        elif wybor == "3":
            klient.koszyk.wyswietl()

        elif wybor == "4":
            produkt_id = int(input("ID produktu: "))

            wybor_usuwania = input("Usunąć cały produkt? (t/n): ").lower()

            if wybor_usuwania == "t":
                klient.koszyk.usun(produkt_id)
            else:
                ilosc = int(input("Ile sztuk usunąć?: "))
                klient.koszyk.usun(produkt_id, ilosc)

            print("Koszyk zaktualizowany.")

        elif wybor == "5":

            kwota = sklep.realizuj_zamowienie(klient)

            print(
                f"Zamówienie zrealizowane. "
                f"Kwota: {kwota:.2f} zł"
            )

        elif wybor == "6":

            print(
                f"Stan konta sklepu: "
                f"{sklep.stan_konta:.2f} zł"
            )

        elif wybor == "7":

            while True:
                menu_magazyn()

                poprawny_wybor_magazyn = False
                while not poprawny_wybor_magazyn:
                    wybor_magazyn = input("Wybierz opcję: ")
                    if wybor_magazyn.isdigit():
                        poprawny_wybor_magazyn = True
                    else:
                        print("Wskaż numer pozycji z menu aplikacji")

                if wybor_magazyn == "1":
                    sklep.magazyn.wyswietl_kategorie()

                elif wybor_magazyn == "2":
                    sklep.magazyn.wyswietl_produkty()

                elif wybor_magazyn == "3":

                    sklep.magazyn.wyswietl_kategorie()

                    kategoria_id = int(input("Podaj ID kategorii: "))

                    sklep.magazyn.wyswietl_produkty_z_kategorii(kategoria_id)

                elif wybor_magazyn == "0":
                    break

                else:
                    print("Nieprawidłowa opcja.")

        elif wybor == "0":
            print("Do widzenia!")
            break

        else:
            print("Nieprawidłowa opcja.")

if __name__ == "__main__":
    main()