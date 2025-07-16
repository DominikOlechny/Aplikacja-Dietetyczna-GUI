#pierwsza warstwa aplikacji odpowiedzialna za logowanie do apki lub tworzenie uzytkownika.

import pandas as pd

def readCSV(): #odczyt pliku CSV
    path_users_info = 'users_info.csv' #plik csv z userami
    return pd.read_csv(path_users_info, delimiter=';') #zwrocenie danych odczytanego pliku csv, delimiterem jest ;.

def writeCSV(users): #zapis do pliku csv
    path_users_info = 'users_info.csv' #plik csv z userami
    users.to_csv(path_users_info, sep=';', index=False) #zapis danych odczytanego pliku csv, delimiterem jest ;.

def register_user(users): #funkcja odpowiedzialna za rejestracje (dodanie konta)
    print("Rejestracja konta")
    username = input("Podaj login: ") #podanie loginu ktory bedzie uzywany do logowania
    while not users[users['Login'] == username].empty: #sprawdzenie czy user juz istnieje i poproszenie o inny login
        print("Login już istnieje. Podaj inny login.")
        username = input("Podaj login: ")
    
    password = input("Podaj hasło: ")  #podanie hasla, przypisanie danych na 0.
    cpm = 0
    protein = 0
    fats = 0
    carbs = 0
    total_cpm = 0
    total_carbs = 0
    total_pal = 0
    total_fats = 0
    
    #stworzenie nowego rekordu w tabeli
    new_user = pd.DataFrame([{ 
        'Login': username,
        'Password': password,
        'CPM': cpm,
        'Protein': protein,
        'Fats': fats,
        'Carbs': carbs,
        'Total_cpm': total_cpm,
        'Total_carbs': total_carbs,
        'Total_pal': total_pal,
        'Total_fats': total_fats
    }])
    
    users = pd.concat([users, new_user], ignore_index=True)
    writeCSV(users) #edycja pliku csv, zapis.
    print("Rejestracja zakończona sukcesem! Możesz teraz się zalogować.")
    return users

def login_user(users): #opcja odwiedzialna za logowanie oraz menu
    choice = 0
    while choice == 0:
        print("Co chcesz wykonać?:")
        print("1. Zalogować się:")
        print("2. Zarejestrować Konto:")
        choice = input("Wybierz 1 albo 2: ")
        if choice == "1":
            while True:
                username = input("Podaj login: ")
                password = input("Podaj hasło: ")

                user = users[(users['Login'] == username) & (users['Password'] == password)]

                if not user.empty:
                    print(f"Witaj, {username}!")
                    log_user = user.iloc[0]  # Pobieramy pierwszego użytkownika, który pasuje do loginu i hasła
            
                    # Przypisywanie danych użytkownika do zmiennych
                    login = log_user['Login']
                    cpm = log_user['CPM']
                    protein = log_user['Protein']
                    fats = log_user['Fats']
                    carbs = log_user['Carbs']
                    total_cpm = log_user['Total_cpm']
                    total_carbs = log_user['Total_carbs']
                    total_pal = log_user['Total_pal']
                    total_fats = log_user['Total_fats']
                    return login, cpm, protein, fats, carbs, total_cpm, total_carbs, total_pal, total_fats #zwrocenie wartosci uzytkownika
                else:
                    print("Niepoprawne dane logowania. Spróbuj ponownie.")
        elif choice == "2":
            users = register_user(users)
            choice = 0  #Reset menu do poczatku po zalogowoaniu
        else:
            print("Niepoprawny wybór. Spróbuj ponownie.")
            choice = 0  #Powrot do poczatku menu
    return None, None, None, None, None, None, None, None, None #zwrocenie pustych danych

def login(username, password):
    users = readCSV()
    user = users[(users['Login'] == username) & (users['Password'] == password)]
    return not user.empty

