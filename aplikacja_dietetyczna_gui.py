import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import login_panel
import addup_calories
import generate_chart
from add_info import info
import os
import sys
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

class DietApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja Dietetyczna")
        self.geometry("400x400")
        self.logged_user = None

        self.username_label = tk.Label(self, text="Login:")
        self.username_label.pack(pady=5)

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Hasło:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self, text="Zaloguj", command=self.login)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self, text="Zarejestruj się", command=self.register_user)
        self.register_button.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if login_panel.login(username, password):
            messagebox.showinfo("Sukces", "Zalogowano poprawnie")
            self.logged_user = username
            self.open_main_panel()
        else:
            messagebox.showerror("Błąd", "Niepoprawne dane logowania")

    def register_user(self):
        register_window = tk.Toplevel(self)
        register_window.title("Rejestracja")
        register_window.geometry("300x250")

        tk.Label(register_window, text="Login:").pack(pady=5)
        username_entry = tk.Entry(register_window)
        username_entry.pack(pady=5)

        tk.Label(register_window, text="Hasło:").pack(pady=5)
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack(pady=5)

        def perform_registration():
            username = username_entry.get()
            password = password_entry.get()
            users = login_panel.readCSV()

            if not users[users['Login'] == username].empty:
                messagebox.showerror("Błąd", "Login już istnieje. Podaj inny.")
                return

            new_user = pd.DataFrame([{ 
                'Login': username,
                'Password': password,
                'CPM': 0,
                'Protein': 0,
                'Fats': 0,
                'Carbs': 0,
                'Total_cpm': 0,
                'Total_carbs': 0,
                'Total_pal': 0,
                'Total_fats': 0
            }])

            users = pd.concat([users, new_user], ignore_index=True)
            try:
                users.to_csv('users_info.csv', sep=';', index=False)
                messagebox.showinfo("Sukces", "Rejestracja zakończona sukcesem!")
                register_window.destroy()
            except PermissionError:
                messagebox.showerror("Błąd", "Plik 'users_info.csv' jest otwarty lub zablokowany.")

        tk.Button(register_window, text="Zarejestruj", command=perform_registration).pack(pady=10)
        tk.Button(register_window, text="Anuluj", command=register_window.destroy).pack(pady=5)

    def open_main_panel(self):
        self.withdraw()
        main_panel = tk.Toplevel(self)
        main_panel.title("Panel Główny")
        main_panel.geometry("400x450")

        tk.Button(main_panel, text="Zarządzaj produktami", command=self.manage_products).pack(pady=10)
        tk.Button(main_panel, text="Zmień parametry konta", command=self.update_user_info).pack(pady=10)
        tk.Button(main_panel, text="Generuj wykres", command=self.generate_chart).pack(pady=10)
        tk.Button(main_panel, text="Wyloguj", command=lambda: [main_panel.destroy(), self.deiconify()]).pack(pady=10)

    def manage_products(self):
        products_window = tk.Toplevel(self)
        products_window.title("Zarządzanie Produktami")
        products_window.geometry("500x450")

        search_label = tk.Label(products_window, text="Szukaj produktu:")
        search_label.pack(pady=5)

        search_entry = tk.Entry(products_window)
        search_entry.pack(pady=5)

        products_list = tk.Listbox(products_window, width=60)
        products_list.pack(pady=10)

        tk.Button(products_window, text="Szukaj", command=lambda: self.search_products(search_entry.get(), products_list)).pack(pady=5)
        tk.Button(products_window, text="Dodaj wybrany produkt", command=lambda: self.add_selected_product(products_list)).pack(pady=5)
        tk.Button(products_window, text="Usuń wybrany produkt", command=lambda: self.remove_selected_product(products_list)).pack(pady=5)
        tk.Button(products_window, text="Odśwież listę", command=lambda: self.refresh_products_list(products_list)).pack(pady=5)
        tk.Button(products_window, text="Powrót", command=products_window.destroy).pack(pady=5)

        self.refresh_products_list(products_list)

    def update_user_info(self):
        update_window = tk.Toplevel(self)
        update_window.title("Aktualizacja parametrów")
        update_window.geometry("300x400")

        tk.Label(update_window, text="Płeć:").pack(pady=5)
        gender_var = tk.StringVar()
        gender_box = ttk.Combobox(update_window, textvariable=gender_var, values=["mężczyzna", "kobieta"])
        gender_box.pack(pady=5)

        tk.Label(update_window, text="Waga (kg):").pack(pady=5)
        weight_entry = tk.Entry(update_window)
        weight_entry.pack(pady=5)

        tk.Label(update_window, text="Wzrost (cm):").pack(pady=5)
        height_entry = tk.Entry(update_window)
        height_entry.pack(pady=5)

        tk.Label(update_window, text="Wiek (lata):").pack(pady=5)
        age_entry = tk.Entry(update_window)
        age_entry.pack(pady=5)

        tk.Label(update_window, text="Poziom aktywności fizycznej:").pack(pady=5)
        activity_level = tk.StringVar()
        activity_box = ttk.Combobox(update_window, textvariable=activity_level, values=[
            "1 - brak (osoba chora, leżąca w łóżku)",
            "2 - mała (praca siedząca)",
            "3 - umiarkowana (praca na stojąco)",
            "4 - duża (aktywność, ćwiczenia)",
            "5 - bardzo duża (codzienna aktywność)",
            "6 - zawodowy sportowiec"
        ])
        activity_box.pack(pady=5)

        def submit_info():
            path_users_info = 'users_info.csv'
            info(
                self.logged_user,
                path_users_info,
                gender_box.get(),
                weight_entry.get(),
                height_entry.get(),
                age_entry.get(),
                activity_box.get()
            )
            messagebox.showinfo("Zaktualizowano", "Dane użytkownika zostały zaktualizowane.")
            update_window.destroy()

        tk.Button(update_window, text="Zapisz", command=submit_info).pack(pady=10)
        tk.Button(update_window, text="Anuluj", command=update_window.destroy).pack(pady=5)

    def search_products(self, query, products_list):
        products_list.delete(0, tk.END)
        matching_products = addup_calories.find_products(query)
        for _, product in matching_products.iterrows():
            products_list.insert(tk.END, product['Nazwa'])

    def add_selected_product(self, products_list):
        selected = products_list.get(tk.ACTIVE)
        if selected:
            product = addup_calories.find_products(selected).iloc[0]
            addup_calories.selected_products.append(product)
            totals = addup_calories.calculate_totals(addup_calories.selected_products)
            try:
                addup_calories.save_totals(totals, self.logged_user)
                messagebox.showinfo("Sukces", f'Produkt "{selected}" został dodany i zapisany.')
            except PermissionError:
                messagebox.showerror("Błąd", "Plik 'users_info.csv' jest otwarty lub zablokowany.")

    def remove_selected_product(self, products_list):
        selected = products_list.get(tk.ACTIVE)
        if selected:
            addup_calories.remove_product(selected, addup_calories.selected_products)
            totals = addup_calories.calculate_totals(addup_calories.selected_products)
            try:
                addup_calories.save_totals(totals, self.logged_user)
                messagebox.showinfo("Sukces", f'Produkt "{selected}" został usunięty i zapisany.')
            except PermissionError:
                messagebox.showerror("Błąd", "Plik 'users_info.csv' jest otwarty lub zablokowany.")

    def refresh_products_list(self, products_list):
        products_list.delete(0, tk.END)
        for product in addup_calories.selected_products:
            products_list.insert(tk.END, product['Nazwa'])

    def generate_chart(self):
        generate_chart.main(self.logged_user)

if __name__ == "__main__":
    app = DietApp()
    app.mainloop()
