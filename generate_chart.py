#czesc aplikacji odpowiedzialna za generacje wykresow makra

from login_panel import readCSV
from add_info import info
import matplotlib.pyplot as plt 

def generate_macro_chart(login):
    # Wczytujemy dane użytkowników
    users = readCSV()
    user = users.loc[users['Login'] == login].iloc[0]
    targets = {
        "KCAL": user['CPM'],
        "WEGLOWODANY": user['Carbs'],
        "BIALKO": user['Protein'],
        "TLUSZCZ": user['Fats']
    }
    totals = {
        "KCAL": user['Total_cpm'],
        "WEGLOWODANY": user['Total_carbs'],
        "BIALKO": user['Total_pal'],
        "TLUSZCZ": user['Total_fats']
    }

    # Tworzymy subplots
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # Lista makroskładników i ich etykiet
    macros = ['KCAL', 'WEGLOWODANY', 'BIALKO', 'TLUSZCZ']
    labels = ['KCAL', 'WEGLOWODANY', 'BIALKO', 'TLUSZCZ']

    # Iteracja po makroskładnikach i rysowanie wykresów
    for ax, macro, label in zip(axs.flatten(), macros, labels):
        categories = ['OCZEKIWANE', 'AKTUALNE']
        values = [targets[macro], totals[macro]]
        colors = ['green', 'blue'] if totals[macro] < targets[macro] else ['green', 'red'] if totals[macro] > targets[macro] else ['green', 'green'] #kolory wykresow, jesli wartosci sa mniejsze niz zakladane to jest niebieski, jesli idelny to zielony a jesli powyzej to czerowny.
        ax.bar(categories, values, color=colors)
        ax.set_title(f'{label} OCZEKIWANE VS AKTUALNE')
        ax.set_ylabel('ILOSC')

    plt.tight_layout()
    plt.show()

def main(login):
    generate_macro_chart(login)