#czesc aplikacji opowiedzialna za obliczanie makra dla zalogowanego uzytkownika.

#CPM = PPM x współczynnik aktywności fizycznej
#Wartość współczynnika aktywności fizycznej	Stopień aktywności fizycznej
#1,2	brak (osoba chora, leżąca w łóżku)
#1,4	mała (osoba wykonująca pracę siedzącą)
#1,6	umiarkowana (osoba wykonująca pracę na stojąco)
#1,75	duża (osoba prowadząca aktywny tryb życia, regularnie ćwicząca)
#2,0	bardzo duża (osoba prowadząca bardzo aktywny tryb życia, codziennie ćwicząca)
#2,4	osoba zawodowo uprawiająca sport

#dla kobiet: PPM = 655,1 + (9,563 x masa ciała w kilogramach) + (1,85 x wzrost w centymetrach) – (4,676 x wiek w latach)
#dla mężczyzn: PPM = 66,473 + (13,752 x masa ciała w kilogramach) + (5,003 x wzrost w centymetrach) – (6,775 x wiek w latach)
import pandas as pd
from login_panel import readCSV, login_user

def get_gender(): #pobranie informacji o plci 


    print("PODAJ PŁEĆ")
    print("1 - mężczyzna")
    print("2 - kobieta")
    
    while True:
        Gender = input()

        # Sprawdzenie czy to liczba
        try:
            Gender = int(Gender)
        except ValueError:
            print("Błąd: Podaj poprawne dane (wybierz 1 lub 2)")
            continue  # Kontynuuj petle
        # Sprawdzenie wyboru płci
        if Gender == 1:
            print("Wybrano płeć mężczyzna")
            return Gender
        elif Gender == 2:
            print("Wybrano płeć kobieta")
            return Gender
        else:
            print("Błąd: Podaj poprawne dane (wybierz 1 lub 2)")
            continue  # Kontynuluj pentle

def get_weight(): #pobranie infromacji o wadze
    while True:
        try:
            Weight = float(input("Podaj swoją wagę: "))
            if Weight > 0:
                return Weight  # Zwróć poprawną wagę
            else:
                print("Podaj prawidłową wagę (wartość powinna być większa od 0)")
        except ValueError:
            print("Błąd: Podaj prawidłową wagę (użyj cyfr)")  # Komunikat o wprowadzeniu blednej opcji, nastepnie funkcja wywalola sie ponownie 

    
def get_height(): #pobranie informacji o wzroscie
    while True:
        try:
            Height = float(input("Podaj swój wzrost: "))
            if Height > 0:
                return Height  # Zwróć poprawny wzrost
            else:
                print("Podaj prawidłowy wzrost (wartość powinna być większa od 0)")
        except ValueError:
            print("Podaj prawidłowy wzrost (użyj cyfr)")  # Komunikat o wprowadzeniu blednej opcji, nastepnie funkcja wywalola sie ponownie 
    
def get_age(): #pobranie informacji o wzroscie
    while True:
        try:
            Age = int(input("Podaj swój wiek: "))
            if Age > 0:
                return Age  # Zwróć poprawny wiek
            else:
                print("Podaj wiek, wartość musi być większa niż 0")
        except ValueError:
            print("Nieprawidłowe dane podaj swój wiek w liczbach")  # Komunikat o wprowadzeniu blednej opcji, nastepnie funkcja wywalola sie ponownie 

def get_movement(): #pobranie informacji o aktywnosci fizycznej
    print("1 - brak (osoba chora, leżąca w łóżku")
    print("2 - mała (osoba wykonująca pracę siedzącą")
    print("3 - umiarkowana (osoba wykonująca pracę na stojąco")
    print("4 - duża (osoba prowadząca aktywny tryb życia, regularnie ćwicząca")
    print("5 - bardzo duża (osoba prowadząca bardzo aktywny tryb życia, codziennie ćwicząca")
    print("6 - osoba zawodowo uprawiająca sport")
    while True:
        Movement = input()

        # Sprawdzenie czy to liczba
        try:
            Movement = int(Movement)
        except ValueError:
            print("Błąd: Podaj poprawne dane (wybierz 1 lub 6)")
            continue  #petla wywylouje sie jeszcze raz aby zapytac o porawna wartosc

        # Sprawdzenie aktywnosci
        if Movement == 1:
            print("brak (osoba chora, leżąca w łóżku)")
            Activity = float(1.2)
            return Activity
        elif Movement == 2:
            print("mała (osoba wykonująca pracę siedzącą)")
            Activity = float(1.4)
            return Activity
        elif Movement == 3:
            print("umiarkowana (osoba wykonująca pracę na stojąco)")
            Activity = float(1.6)
            return Activity
        elif Movement == 4:
            print("duża (osoba prowadząca aktywny tryb życia, regularnie ćwicząca)")
            Activity = float(1.75)
            return Activity
        elif Movement == 5:
            print("bardzo duża (osoba prowadząca bardzo aktywny tryb życia, codziennie ćwicząca)")
            Activity = float(2)
            return Activity
        elif Movement == 6:
            print("osoba zawodowo uprawiająca sport")
            Activity = float(2.4)
            return Activity
        else:
            print("Błąd: Podaj poprawne dane (wybierz 1 lub 6)")
            continue  #petla wywylouje sie jeszcze raz aby zapytac o porawna wartosc


def get_CPM(gender, weight, hight, age, activity): #OPLICZANIE CPM I PPM
    #PPM przemiana materii
    #dla kobiet: PPM = 655,1 + (9,563 x masa ciała w kilogramach) + (1,85 x wzrost w centymetrach) – (4,676 x wiek w latach)
    #dla mężczyzn: PPM = 66,473 + (13,752 x masa ciała w kilogramach) + (5,003 x wzrost w centymetrach) – (6,775 x wiek w latach)1
   
    if(gender == 1):
        PPM = 66.473 + (13.752 * weight) + (5.003 * hight) - (6.775 * age)
    else:
        PPM = 655.1 + (9.563 * weight) + (1.85 * hight) - (4.676 * age)
    CPM=PPM*activity
    return CPM #ilosc kilokalorii

def get_PAL(weight, activity): #Dzienne zapotrzebowanie na białko
    pal_factors = {
        1.2: 1.2, 1.4: 1.3, 1.6: 1.4, 1.75: 1.5, 2.0: 1.7, 2.4: 2.0
    }
    protein_requirement = pal_factors[activity] * weight
    return protein_requirement

def get_fats(CPM): #Dzienne zapotrzebowanie na tłuszcz
    fats = (CPM - (CPM * 0.75)) / 9
    return fats

def get_carbs(CPM): #obliczanie zapotrzebowania na weglowodany
    carbs = CPM*0.5/4 #ze wzoru kcal*50%/4
    return carbs

def info(login, path, gender, weight, height, age, activity):
    users = pd.read_csv(path, delimiter=';')
    user_index = users[users['Login'] == login].index[0]

    # Konwersja danych
    gender = gender.lower()
    weight = float(weight)
    height = float(height)
    age = int(age)
    activity = int(activity[0])  # np. "1 - brak ..." → 1

    # Obliczanie BMR i CPM
    if gender == 'mężczyzna':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    pal_factors = [1.2, 1.4, 1.6, 1.75, 2.0, 2.3]
    pal = pal_factors[activity - 1]
    cpm = bmr * pal

    # Obliczanie makroskładników
    protein = weight * 2  # 2g na kg
    fats = weight * 1     # 1g na kg
    carbs = (cpm - (protein * 4 + fats * 9)) / 4

    # Aktualizacja danych w DataFrame
    users.loc[user_index, 'CPM'] = round(cpm, 2)
    users.loc[user_index, 'Protein'] = round(protein, 2)
    users.loc[user_index, 'Fats'] = round(fats, 2)
    users.loc[user_index, 'Carbs'] = round(carbs, 2)

    # Zapis do pliku
    users.to_csv(path, sep=';', index=False)