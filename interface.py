import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import bcrypt
from database import *
from api import *
from datetime import datetime
from classuseful import AlerteExistante
from functools import partial


class CryptoApp:
    def __init__(self, root):
        self.root = root


        # Initialisation de l'écran
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.clear_screen()

        # Bienvenue
        welcome_label = tk.Label(self.root, text="Bienvenue dans l'application de Cryptomonnaies", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=20)

        signup_with_email_button = tk.Button(self.root, text="S'inscrire", command=self.create_signup_screen,bg="blue", fg="white", font=("Arial", 12))
        signup_with_email_button.pack(pady=10, fill=tk.X, padx=50)

        login_button = tk.Button(self.root, text="Se connecter", command=self.create_login_screen, bg="green", fg="white", font=("Arial", 12))
        login_button.pack(pady=10, fill=tk.X, padx=50)

    def create_login_screen(self):
        self.clear_screen()

        # Titre de connexion
        login_label = tk.Label(self.root, text="Connexion", font=("Arial", 16, "bold"))
        login_label.pack(pady=20)

        # Entrée pour email
        email_label = tk.Label(self.root, text="Email:")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        # Entrée pour mot de passe
        password_label = tk.Label(self.root, text="Mot de Passe:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # Bouton de connexion
        login_button = tk.Button(self.root, text="Se connecter", command=self.login, bg="green", fg="white")
        login_button.pack(pady=10)

        # Retour à l'écran précédent
        back_button = tk.Button(self.root, text="Retour", command=self.create_welcome_screen)
        back_button.pack(pady=10)
        
    def create_signup_screen(self):
        self.clear_screen()

        # Titre d'inscription
        signup_label = tk.Label(self.root, text="Inscription", font=("Arial", 16, "bold"))
        signup_label.pack(pady=20)

        # Entrée pour email
        email_label = tk.Label(self.root, text="Email:")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        # Entrée pour mot de passe
        password_label = tk.Label(self.root, text="Mot de Passe:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        # Bouton d'inscription
        signup_button = tk.Button(self.root, text="S'inscrire", command=self.signup_with_email, bg="blue", fg="white")
        signup_button.pack(pady=10)

        # Bouton de retour à l'écran d'accueil
        back_button = tk.Button(self.root, text="Retour", command=self.create_welcome_screen)
        back_button.pack(pady=10)


    def login(self):

        email = self.email_entry.get()
        password = self.password_entry.get()
        
        user = get_user(email)
        if user:
            stored_password = user[2]  # La colonne 'password'
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                messagebox.showinfo("Connexion réussie", "Vous êtes connecté !")
                self.create_main_screen()
            else:
                messagebox.showerror("Erreur", "Mot de passe incorrect.")
        else:
            messagebox.showerror("Erreur", "Utilisateur non trouvé.")

    def signup_with_email(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return
        
        try:
            add_user(email, password)
            messagebox.showinfo("Succès", "Inscription réussie. Vous pouvez maintenant vous connecter.")
            self.create_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erreur", "Cet email est déjà enregistré.")
            
    # Fonction pour récupérer les données de la base
    def get_all_crypto_with_threshold(self):
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()
        
        # Requête pour récupérer la monnaie et son seuil
        cursor.execute("""
            SELECT Cryptomonnaies.cryptomonnaie, Alertes.seuil
            FROM Alertes
            JOIN Cryptomonnaies ON Alertes.crypto_id = Cryptomonnaies.id
        """)
    
        results = cursor.fetchall()  # Retourne une liste de tuples (monnaie, seuil)
        connection.close()
        
        return results


    def alerts_screen(self):
        """Affiche la liste des alertes avec un bouton retour."""
        self.clear_screen()  # Efface l'écran avant d'afficher les nouvelles alertes

        frame_tableau = tk.Frame(self.root)
        frame_tableau.pack(pady=10, padx=20)

        cryptos = self.get_all_crypto_with_threshold()
        print("Alertes récupérées:", cryptos)  # Debug pour vérifier les données

        if not cryptos:
            tk.Label(self.root, text="Aucune alerte enregistrée.", fg="red").pack()
        else:
            # Ajouter les en-têtes
            tk.Label(frame_tableau, text="Monnaie", width=15, borderwidth=1, relief="solid").grid(row=0, column=0)
            tk.Label(frame_tableau, text="Seuil", width=15, borderwidth=1, relief="solid").grid(row=0, column=1)
            tk.Label(frame_tableau, text="Actions", width=15, borderwidth=1, relief="solid").grid(row=0, column=2)

            # Ajouter chaque crypto avec son seuil
            for i, (monnaie, seuil) in enumerate(cryptos, start=1):
                tk.Label(frame_tableau, text=monnaie, width=15, borderwidth=1, relief="solid").grid(row=i, column=0)
                tk.Label(frame_tableau, text=seuil, width=15, borderwidth=1, relief="solid").grid(row=i, column=1)

                # Correction : Utilisation de `partial` pour capturer les valeurs correctes
                delete_button = tk.Button(frame_tableau, text="Supprimer", bg="red", fg="white",
                                          command=partial(self.on_delete, monnaie, seuil))
                delete_button.grid(row=i, column=2)

        # Bouton Retour
        back_button = tk.Button(self.root, text="Retour", bg="gray", fg="white", command=lambda: self.create_main_screen())
        back_button.pack(pady=10)


            
    def on_delete(self,monnaie, seuil):
        response = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer l'alerte {monnaie} avec le seuil {seuil} ?")
        if response:  # Si confirmé
            delete_alerte(monnaie, seuil)
            self.alerts_screen()   
        
    def create_main_screen(self):
        self.clear_screen()

        # Titre
        title = tk.Label(self.root, text="Suivi des Cryptomonnaies", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # Variables
        self.crypto = tk.StringVar()
        self.price_alert = tk.StringVar()
        self.volume_alert = tk.StringVar()

        # Frame pour les entrées
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Sélection de la cryptomonnaie
        tk.Label(frame, text="Choisir une cryptomonnaie:").grid(row=0, column=0, padx=5, pady=5)
        self.crypto_combobox = ttk.Combobox(frame, textvariable=self.crypto, state="readonly")
        self.crypto_combobox['values'] = ['OKCOINUSD_SPOT_BTC_USD', 'COINBASE_SPOT_BTC_USD']
        if not self.crypto_combobox['values']:
            messagebox.showinfo("une erreur s'est produite, réésayez ultérieurement ,merci")
        self.crypto_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Entrée pour le prix d'alerte
        tk.Label(frame, text="Prix d'alerte:").grid(row=1, column=0, padx=5, pady=5)
        self.price_entry = tk.Entry(frame, textvariable=self.price_alert)
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)


        # Bouton pour ajouter une alerte
        try:
            add_alert_button = tk.Button(self.root, text="Ajouter une alerte", command=lambda: add_alerte(self.crypto_combobox.get(), self.price_alert.get()), bg="green", fg="white")
        except AlerteExistante as e:
            messagebox.showinfo("{e}")
        add_alert_button.pack(pady=10, fill=tk.X, padx=20)

        # Boutons pour les notifications et arrêter les alertes
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10, fill=tk.X, padx=20)

        show_notif_button = tk.Button(button_frame, text="Afficher mes alertes", command=self.alerts_screen)
        show_notif_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        stop_alerts_button = tk.Button(button_frame, text="Déconnexion", command=self.create_welcome_screen, bg="red", fg="white")
        stop_alerts_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def add_alert(self):
        crypto = self.crypto.get()
        price = self.price_alert.get()
        print(f"Ajouter une alerte : {crypto}, Prix : {price}")

        
        
if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Application Crypto")

    frame_tableau = tk.Frame(root)  # Créer frame_tableau ici
    frame_tableau.pack(pady=20)
    
    # 🔹 Initialisation de l'interface
    app = CryptoApp(root)


    #  Lancement du processus de mise à jour sans bloquer l'UI
    root.after(5000, lambda: verifier_alertes(root))  # Passer root en argument

    root.mainloop()


    

