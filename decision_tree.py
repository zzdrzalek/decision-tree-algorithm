import math
import json

def odczytanie_wierszy_z_pliku(plik):
    """
    Funkcja odczytująca dane w postaci wierwszy z pliku tekstoweg
    :param plik: plik z którego czytamy tablice danych
    :return: wszystkie_wierwsze tablicy
    """
    with open(plik, "r") as plik:
        wszystkie_wiersze = []
        for wiersz in plik:
            wiersz = wiersz.strip().split(',')
            lista2 = []
            for el in wiersz:
                try:
                    lista2.append(int(el))
                except:
                    lista2.append(el)
            wszystkie_wiersze.append(lista2)
        return wszystkie_wiersze


def wiersze_na_kolumny(wszystkie_wiersze):
    """
    Funckja prekształcająca wiersze na kolumny
    :param lista_wierszy: lista wierszy, które przekształcone zostaną na liste kolumn
    :return: lista kolumn
    """
    wszystkie_kolumny = []
    for i in range(len(wszystkie_wiersze[0])):
        kolumny = []
        for k in wszystkie_wiersze:
            kolumny.append(k[i])
        wszystkie_kolumny.append(kolumny)
    return wszystkie_kolumny


def liczba_wystapien(wszystkie_kolumny):
    """
    Funkcja zliczająca liczbę wystąpień poszczególnych elementów kolumny
    :param wszystkie_kolumny: wszystkie kolumny
    :return: lista slownik liczby wystapien
    """
    lista_dic = []
    for i in wszystkie_kolumny:
        s = {}
        for j in i:
            s[j] = i.count(j)
        lista_dic.append(s)
    return lista_dic


def prawd_ze_slownika(slownik):
    """
    Funkcja zliczająca prawdopodobieństwo ze słownika
    :param slownik: slownik zliczonych wystapien
    :return: lista prawdopodobienstw
    """
    decyzja_lista = []
    ile = sum(slownik.values())
    for i in slownik.values():
        p = i / ile
        decyzja_lista.append(p)
    return decyzja_lista


def entropia(lista):
    """
    Funkcja wyliczająca entropie
    :param lista: lista prawdopodobienstw
    :return: entropia
    """
    suma = 0
    for i in lista:
        obl = math.log2(i) * i
        suma += obl
    entropia = -suma
    return entropia


def na_slownik_liczby_wystapien(lista):
    """
    Funkcja zmieniająca listę wystąpień na słownik
    :param lista: lista wystąpień
    :return: slownik
    """
    slownik_pom1 = {}
    for i in lista:
        if i not in slownik_pom1.keys():
            slownik_pom1[i] = 1
        else:
            slownik_pom1[i] += 1
    return slownik_pom1


def lista_informacji_dla_atrybutow(wszystkie_kolumny, wszystkie_wiersze,
                                   lista_slownikow_liczby_wystapien):
    """
    Funkcja obliczająca informację dla każdego atrybutu
    :param wszystkie_kolumny: wszystkie kolumny
    :param wszystkie_wiersze: wszystkie wiersze
    :param lista_slownikow_liczby_wystapien: slownik z liczba wystapien
    :return: lista informacji dla atrybutow
    """
    lista_informacji_dla_atr = []
    for atrybut in range(len(wszystkie_kolumny) - 1):
        slownik_pom = {}
        for s in lista_slownikow_liczby_wystapien[atrybut].keys():
            slownik_pom[s] = []
        for wiersz in wszystkie_wiersze:
            for wartosc in set(wszystkie_kolumny[atrybut]):
                try:
                    if wartosc == wiersz[atrybut]:
                        slownik_pom[wartosc].append(wiersz[-1])
                except IndexError:
                    pass

        lista_prawd = prawd_ze_slownika(lista_slownikow_liczby_wystapien[atrybut])
        lista_entropii = []
        for klucz in slownik_pom.keys():
            lista_entropii.append(entropia(
                prawd_ze_slownika(na_slownik_liczby_wystapien(slownik_pom[klucz]))))
        info = 0
        for j in range(len(lista_entropii)):
            info += lista_entropii[j] * lista_prawd[j]
        lista_informacji_dla_atr.append(info)
    return lista_informacji_dla_atr


def przyrost_informacji(entropia_zbioru, lista_informacji_dla_atr):
    """
    Funkcja zwracająca przyrost informacji
    :param entropia_zbioru: entropia dla każdego atrybutu
    :param lista_indormacji_dla_atr: informacja dla każdego atrybutu
    :return: lista przyrostu informacji dla kazdego atrybutu
    """
    przyrost_info = [(entropia_zbioru - info) for info in lista_informacji_dla_atr]
    return przyrost_info


def zrownowazony_przyrost_1(wszystkie_kolumny, przyrost_info):
    """
    Funkcja zwracająca zrownowazony przyrost dla kazdego atrybutu
    :param wszystkie_kolumny: wszystkie kolumny
    :param przyrost_info: przyrost informacji dla wszystkich atrybutow
    :return: zrownowazony przyrost informacji
    """
    lista_zrow_przyrost = []
    lista_pom = []
    for i in wszystkie_kolumny[:-1]:
        ent = entropia(prawd_ze_slownika(na_slownik_liczby_wystapien(i)))
        lista_pom.append(ent)
    for i in range(len(lista_pom)):
        try:
            lista_zrow_przyrost.append(przyrost_info[i] / lista_pom[i])
        except ZeroDivisionError:
            lista_zrow_przyrost.append(0)
    return lista_zrow_przyrost


def wybor_najlepszego_podzialu(lista_zrow_przyrostu):
    return lista_zrow_przyrostu.index(max(lista_zrow_przyrostu))


def podziel_wedlug_max(wszystkie_wiersze, atrybut):
    podatrybuty = set()
    lista_list_po_podziale = []

    for wiersz in wszystkie_wiersze:
        podatrybuty.add(wiersz[atrybut])

    for i in list(podatrybuty):
        podlista = []
        for j in wszystkie_wiersze:
            if i == j[atrybut]:
                podlista.append(j)
        lista_list_po_podziale.append(podlista)

    return lista_list_po_podziale, podatrybuty




def zbuduj_drzewo(wszystkie_wiersze, poziom = 0):
    galezie = {}
    wszystkie_kolumny = wiersze_na_kolumny(wszystkie_wiersze)
    lista_slownikow_liczby_wystapien = liczba_wystapien(wszystkie_kolumny)
    decyzja = lista_slownikow_liczby_wystapien[-1]
    listaa = prawd_ze_slownika(decyzja)
    entropia_zbioru = entropia(listaa)
    lista_informacji_dla_atr = lista_informacji_dla_atrybutow(wszystkie_kolumny,wszystkie_wiersze, lista_slownikow_liczby_wystapien)
    przyrost_info = przyrost_informacji(entropia_zbioru, lista_informacji_dla_atr)
    zrownowazony_przyrost = zrownowazony_przyrost_1(wszystkie_kolumny, przyrost_info)
    atrybut = wybor_najlepszego_podzialu(zrownowazony_przyrost)
    galaz, podatrybuty1 = podziel_wedlug_max(wszystkie_wiersze, atrybut)


    if max(zrownowazony_przyrost) > 0:
        for i in range(len(galaz)):
            galezie[" poziom " + str(poziom) +" dzielimy po atrybucie" + str(atrybut + 1) + " WARTOSC: " + str(galaz[i][0][atrybut])] = zbuduj_drzewo(galaz[i],poziom+1)
    else:
        galezie = wszystkie_kolumny[-1][-1]

    return galezie


wszystkie_wiersze = odczytanie_wierszy_z_pliku("dane_rzecz.data")
drzewo = zbuduj_drzewo(wszystkie_wiersze)
json_object = json.dumps(drzewo) #zmieniamy na objekt json
parsed = json.loads(json_object) #zmieniamy na slownik
print(json.dumps(parsed, indent=4, sort_keys=True))
print("*" * 100)
