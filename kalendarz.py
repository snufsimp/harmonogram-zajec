from dataclasses import dataclass
import json
import os
import time
from tabulate import tabulate

def wyliczanie_minut(godzina):
# funkcja zamienia podane godziny na minuty
    pierwsza_czesc_godziny = godzina.split(":")[0]
    druga_czesc_godziny = godzina.split(":")[1]
    minuty = int(pierwsza_czesc_godziny) * 60 + int(druga_czesc_godziny)
    return minuty

class Kalendarz:
    def __init__(self):
        self.dni_tygodnia = {
            "Poniedziałek": [],
            "Wtorek": [],
            "Środa": [],
            "Czwartek": [],
            "Piątek": [],
            "Sobota": [],
            "Niedziela": []
        }

    def zrob_liste_lekcji(self):
# funkcja robi liste lekcji w kalendarzu, nastepnie mozna ją uzyc
        for dzien, lekcje in self.dni_tygodnia.items():
            if lekcje:
                for i, lekcja in enumerate(lekcje, start=1):
                    print(f"{dzien}, {i}. lekcja: {lekcja["przedmiot"]}, godziny: {lekcja["godzina_start"]} do {lekcja["godzina_koniec"]}")
        while True:
            dzien_lekcji = input("Podaj dzień tygodnia: ")
            numer = int(input("Podaj numer lekcji, którą chcesz zobaczyć: "))
            for dzien, lekcje in self.dni_tygodnia.items():
                if dzien.lower() == dzien_lekcji.lower() and lekcje and 1 <= numer:
                    lekcja = lekcje[numer - 1]
                    return lekcja


    def czy_powtarzane(self, lekcja):
# funkcja sprawdza, czy lekcja, którą próbujemy zapisać nie nachodzi na inną lekcję (w założeniach jest to niemożliwe)
        for dzien in self.dni_tygodnia[lekcja["dzien_tygodnia"]]:
            if dzien["minuty_start"] < lekcja["minuty_koniec"] < dzien["minuty_koniec"]:
                print("Lekcja o takiej godzinie już istnieje, usuń lub edytuj poprzednią")
                return True
            elif lekcja["minuty_start"] > dzien["minuty_start"] and lekcja["minuty_koniec"] < dzien["minuty_koniec"]:
                print("Lekcja o takiej godzinie już istnieje, usuń lub edytuj poprzednią")
                return True
            elif lekcja["minuty_start"] < dzien["minuty_koniec"] < lekcja["minuty_koniec"]:
                print("Lekcja o takiej godzinie już istnieje, usuń lub edytuj poprzednią")
                return True
            elif lekcja["minuty_start"] == dzien["minuty_start"] and lekcja["minuty_koniec"] == dzien["minuty_start"]:
                print("Lekcja o takiej godzinie już istnieje, usuń lub edytuj poprzednią")
                return True
            elif lekcja["minuty_start"] == dzien["minuty_start"] or lekcja["minuty_koniec"] == dzien["minuty_start"]:
                print("Lekcja o takiej godzinie już istnieje, usuń lub edytuj poprzednią")
                return True
        return False

    def usun_lekcje(self, lekcja):
# funkcja usuwa lekcję, która została zaznaczona
        for dzien in self.dni_tygodnia[lekcja["dzien_tygodnia"]]:
            if dzien["godzina_start"] == lekcja["godzina_start"] and dzien["godzina_koniec"] == lekcja["godzina_koniec"] and dzien["dzien_tygodnia"] == lekcja["dzien_tygodnia"]:
                self.dni_tygodnia[lekcja["dzien_tygodnia"]].remove(dzien)
                print("Lekcja została usunięta")
                return

    def edytuj_lekcje(self, lekcja, nowe_dane):
# funkcja pozwala na edytowanie lekcji
        if "minuty_start" not in nowe_dane:
            nowe_dane["minuty_start"] = wyliczanie_minut(nowe_dane["godzina_start"])
        if "minuty_koniec" not in nowe_dane:
            nowe_dane["minuty_koniec"] = wyliczanie_minut(nowe_dane["godzina_koniec"])
        powtarzajacy_sie_dzien = False
        for dzien in self.dni_tygodnia[lekcja["dzien_tygodnia"]]:
# to nie moze tak byc bo wtedy we wtorek mamy lekcje ktora ma w dzien_tygodnia sroda
            if dzien["godzina_start"] == lekcja["godzina_start"] and dzien["godzina_koniec"] == lekcja["godzina_koniec"]:
                if self.czy_powtarzane(nowe_dane):
                    print("Lekcja powtarza się, edycja nie doszła do skutku")
                    return
                else:
                    print("Lekcja została zmieniona")
                    self.usun_lekcje(lekcja)
                    self.dodawanie_lekcji(nowe_dane)
            else:
                print("Podana lekcja nie istnieje")
                return

    def tworzenie_lekcji(self):
# funkcja tworzy lekcje, ktora pozniej mozna dodac do kalendarza, po czym edytowac
        dzien_tygodnia = input("Podaj dzień tygodnia (Poniedziałek, Wtorek, Środa, Czwartek, Piątek, Sobota, Niedziela): ").title()
        godzina_start = input("Podaj godzinę rozpoczęcia zajęć (np. 11:00): ").title()
        godzina_koniec = input("Podaje godzinę zakończenia zajęć(np. 12:00): ").title()
        przedmiot = input("Podaj nazwę przedmiotu: ").title()
        nowy_wpis = {"godzina_start": godzina_start, "godzina_koniec": godzina_koniec, "dzien_tygodnia": dzien_tygodnia, "przedmiot": przedmiot}
        return nowy_wpis


    def dodawanie_lekcji(self, lekcja):
# funkcja dodaje lekcje, używając funkcji wyliczanie_minut dodaje w jakiej minucie dnia zaczyna i kończy się dana lekcja
        lekcja["minuty_start"] = wyliczanie_minut(lekcja["godzina_start"])
        lekcja["minuty_koniec"] = wyliczanie_minut(lekcja["godzina_koniec"])
        if self.czy_powtarzane(lekcja):
            print("Lekcja istnieje już w podanych godzinach, usuń lub edytuj poprzednią, aby dodać nową")
        else:
            self.dni_tygodnia[lekcja["dzien_tygodnia"]].append(lekcja)
            print("Lekcja została dodana")

    def wyswietl_kalendarz(self):
        dni = list(self.dni_tygodnia.keys())
        tabela = []
        ilosc_wierszy = max(len(self.dni_tygodnia[dzien]) for dzien in dni)
        for i in range(ilosc_wierszy):
            wiersz = []
            for dzien in dni:
                if i < len(self.dni_tygodnia[dzien]):
                    lekcja = self.dni_tygodnia[dzien][i]
                    wiersz.append(f"{lekcja['przedmiot']} ({lekcja['godzina_start']} do {lekcja['godzina_koniec']})")
                else:
                    wiersz.append("")
            tabela.append(wiersz)
        print(tabulate(tabela, headers=dni, tablefmt="rounded_outline"))


    def stworz_plik_uzytkownika(self, nazwa_uzytkownika):
# tworzy plik json o nazwie uzytkownika podanej na poczatku programu gdzies nazwa_uzytkownika = input(f"Podaj nazwę użytkownika:")
        nazwa_pliku_json = f"{nazwa_uzytkownika}.json"
        if not os.path.exists(nazwa_pliku_json):
            data = self.dni_tygodnia
            with open(nazwa_pliku_json, 'w') as file:
                json.dump(data, file)
                print(f"Utworzono plik {nazwa_pliku_json} dla {nazwa_uzytkownika}")
        elif os.path.exists(nazwa_pliku_json):
            print("Plik o nazwie tego użytkownika istnieje, otwieram")
            with open(nazwa_pliku_json, 'r') as file:
                data = json.load(file)
                self.dni_tygodnia = data

    def zapisz_kalendarz(self, nazwa_uzytkownika):
# zapisuje caly kalendarz w pliku podanego uzytkownika
        nazwa_pliku_json = f"{nazwa_uzytkownika}.json"
        data = self.dni_tygodnia
        with open(nazwa_pliku_json, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Kalendarz został zapisany do twojego pliku {nazwa_pliku_json}")

    def co_robimy(self):
        print("1. Wyświetl kalendarz")
        print("2. Utwórz lekcję")
        print("3. Edytuj lekcję")
        print("4. Usuń lekcję")
        print("5. Zakończ")
        odpowiedz = input("Co chcesz zrobić? ")
        if odpowiedz == "1":
            print("Oto twój kalendarz:")
            self.wyswietl_kalendarz()
            self.co_robimy()
        elif odpowiedz == "2":
            dodawana_lekcja = self.tworzenie_lekcji()
            self.dodawanie_lekcji(dodawana_lekcja)
            self.co_robimy()
        elif odpowiedz == "3":
            edytowana_lekcja = self.zrob_liste_lekcji()
            nowa_lekcja = self.tworzenie_lekcji()
            self.edytuj_lekcje(edytowana_lekcja, nowa_lekcja)
            self.co_robimy()
        elif odpowiedz == "4":
            usuwana_lekcja = self.zrob_liste_lekcji()
            self.usun_lekcje(usuwana_lekcja)
            self.co_robimy()
        elif odpowiedz == "5":
            return
        else:
            print("Twoja odpowiedź jest niepoprawna, czy na pewno użyłeś prawidłowego formatu? (np. 1)")
            self.co_robimy()


def main():


    kalendarz = Kalendarz()
    nazwa_uzytkownika = input("Podaj nazwę użytkownika: ")
    kalendarz.stworz_plik_uzytkownika(nazwa_uzytkownika)
    kalendarz.co_robimy()
    kalendarz.zapisz_kalendarz(nazwa_uzytkownika)

if __name__ == "__main__":
    main()