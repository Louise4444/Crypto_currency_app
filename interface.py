import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import bcrypt
from database import *
from api import *


class CryptoApp:
    def __init__(self, root):
        self.root = root
        self.current_user = None  # Stocke l'utilisateur connecté
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.clear_screen()

        # Bienvenue
        welcome_label = tk.Label(self.root, text="Welcom to the cryptocurrency app", font=("Arial", 16, "bold"))
        welcome_label.pack(pady=20)

        signup_with_email_button = tk.Button(self.root, text="Signup / S'inscrire", command=self.create_signup_screen,bg="blue", fg="white", font=("Arial", 12))
        signup_with_email_button.pack(pady=10, fill=tk.X, padx=50)

        login_button = tk.Button(self.root, text="Login / Se connecter", command=self.create_login_screen, bg="green", fg="white", font=("Arial", 12))
        login_button.pack(pady=10, fill=tk.X, padx=50)

    def create_login_screen(self):
        self.clear_screen()

        login_label = tk.Label(self.root, text="Connexion", font=("Arial", 16, "bold"))
        login_label.pack(pady=20)

        email_label = tk.Label(self.root, text="Email:")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5, fill=tk.X, padx=50)

        password_label = tk.Label(self.root, text="Password / Mot de Passe:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5, fill=tk.X, padx=50)

        login_button = tk.Button(self.root, text="Login / Se connecter", command=self.login, bg="green", fg="white")
        login_button.pack(pady=10, fill=tk.X, padx=50)

        # Bouton Retour bien visible
        back_button = tk.Button(self.root, text="Back / Retour", command=self.create_welcome_screen)
        back_button.pack(pady=10, fill=tk.X, padx=50)
        
    def create_signup_screen(self):
        self.clear_screen()

        # Titre d'inscription
        signup_label = tk.Label(self.root, text="Registration / Inscription", font=("Arial", 16, "bold"))
        signup_label.pack(pady=20)
        
        #Entrée pour pseudo
        pseudo_label = tk.Label(self.root, text="username / nom d'utilisateur:")
        pseudo_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5, fill=tk.X, padx=50)
        
        # Entrée pour email
        email_label = tk.Label(self.root, text="Email:")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5, fill=tk.X, padx=50)
        
        # Entrée pour mot de passe
        password_label = tk.Label(self.root, text="Password / Mot de Passe:")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5, fill=tk.X, padx=50)

        # Bouton d'inscription
        signup_button = tk.Button(self.root, text="Sign up / S'inscrire", command=self.signup_with_email, bg="blue", fg="white")
        signup_button.pack(pady=10)

        # Bouton de retour à l'écran d'accueil
        back_button = tk.Button(self.root, text="Back / Retour", command=self.create_welcome_screen)
        back_button.pack(pady=10)


    def login(self):

        email = self.email_entry.get()
        password = self.password_entry.get()
        
        self.current_user = get_user(email)
        if self.current_user:
            stored_password = self.current_user[3]  # La colonne 'password'
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                messagebox.showinfo("Connexion réussie", "Vous êtes connecté !")
                self.create_main_screen()
            else:
                messagebox.showerror("Error", "Mot de passe incorrect.")
        else:
            messagebox.showerror("Error", "Utilisateur non trouvé.")

    def signup_with_email(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if not username or not email or not password:
            messagebox.showerror("Error", "Veuillez remplir tous les champs.")
            return

        # Vérification de l'existence de l'email dans la base de données
        if get_user(email):
            messagebox.showerror("Error", "Cet email est déjà enregistré.")
            return

        try:
            add_user(username, email, password)
            messagebox.showinfo("Succès", "Inscription réussie. Vous pouvez maintenant vous connecter.")
            self.create_login_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Une erreur est survenue : {e}")

    def create_alerts_screen(self):
        """Affiche les alertes de l'utilisateur sous forme de tableau"""
        self.clear_screen()  # Efface l'écran précédent

        # Titre
        title_label = tk.Label(self.root, text="Mes Alertes", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)

        # Création du tableau (Treeview)
        columns = ("Cryptomonnaie", "Prix", "Seuil", "Type d'Alerte")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")

        # Définition des en-têtes
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=120)  # Ajuste la largeur des colonnes

        # Récupération des alertes de l'utilisateur
        alerts = collect_alerts(self.current_user[0])  # [(crypto, price, seuil, alert_type), ...]

        # Ajout des alertes dans le tableau
        for alert in alerts:
            tree.insert("", "end", values=alert)

        tree.pack(pady=10, fill="both", expand=True)

        # Bouton de retour
        back_button = tk.Button(self.root, text="Retour", command=self.create_main_screen)
        back_button.pack(pady=10, fill=tk.X, padx=50)


    def delete_alert_button(self, crypto, seuil, alert_type):  
        response = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer l'alerte pour {crypto} de type {alert_type} et comme seuil {seuil} ")
        if response:  # Si confirmé
            delete_alerte(self.current_user[0,crypto,seuil,alert_type])
            self.create_alerts_screen
                    
    def create_main_screen(self):
        self.clear_screen()

        # Titre (utilise grid ici aussi)
        title = tk.Label(self.root, text=f"Bonjour {self.current_user[1]}", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, pady=10, columnspan=2)  # Utiliser grid ici au lieu de pack

        # Variables
        self.crypto = tk.StringVar()
        self.seuil = tk.StringVar()
        self.alert_type = tk.StringVar()

        # Frame pour les entrées
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=1, column=0, padx=10, pady=10, columnspan=2)  # Utilisation de grid pour le frame

        # Sélection de la cryptomonnaie
        tk.Label(self.frame, text="Cryptomonnaie:").grid(row=0, column=0, padx=5, pady=5, sticky="w")  # "w" pour aligner à gauche
        self.crypto_combobox = ttk.Combobox(self.frame, textvariable=self.crypto, state="normal", width=30)
        available_crypto=collect_crypto_list()
        self.crypto_combobox['values'] = available_crypto
        self.crypto_combobox.grid(row=0, column=1, padx=5, pady=5)

        # Ajouter un événement pour filtrer les résultats de la combobox
        self.crypto_combobox.bind("<KeyRelease>", self.filter_combobox)

        # Entrée pour le prix d'alerte
        tk.Label(self.frame, text="Prix d'alerte:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.price_entry = tk.Entry(self.frame, textvariable=self.seuil, width=30)  
        self.price_entry.grid(row=1, column=1, padx=5, pady=5)

        # Type d'alerte
        tk.Label(self.frame, text="Type d'alerte:").grid(row=2, column=0, padx=5, pady=5, sticky="w")  
        self.alert_type_combobox = ttk.Combobox(self.frame, textvariable=self.alert_type, state="readonly", width=30)  
        self.alert_type_combobox['values'] = ["Égal", "Au-dessus", "Au-dessous"]
        self.alert_type_combobox.grid(row=2, column=1, padx=5, pady=5)

        # Création du bouton d'ajout d'alerte
        add_alert_button = tk.Button(self.root, text="Ajouter une alerte", command=self.adding_alert_button, bg="green", fg="white")
        add_alert_button.grid(row=3, column=0, columnspan=2, pady=10, padx=20, sticky="ew")  
        
        
        #afficher les alertes creer 
        show_notif_button = tk.Button(self.root, text="Afficher mes alertes", command=self.create_alerts_screen,bg="blue", fg="white", font=("Arial", 12))
        show_notif_button.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="ew")
        
        logout_button = tk.Button(self.root, text="Déconnexion", command=self.create_welcome_screen, bg="red", fg="white")
        logout_button.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="ew") 


    def filter_combobox(self, event):
        """Filtre les options de la combobox en fonction de l'entrée"""
        search_term = self.crypto.get().lower()  # Récupère ce qui a été tapé
        
        # Si le champ de recherche est vide, remettre toutes les cryptos
        if not search_term:
            self.crypto_combobox['values'] = collect_crypto_list()
        else:
            # Filtrer les cryptos en fonction du texte tapé
            filtered_cryptos = [crypto for crypto in self.crypto_combobox['values'] if search_term in crypto.lower()]
            # Mettre à jour les valeurs de la combobox
            self.crypto_combobox['values'] = filtered_cryptos
            
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def adding_alert_button(self):
        crypto_value = self.crypto.get().strip()
        seuil_value = self.seuil.get().strip()
        alert_type_value = self.alert_type.get().strip()

        if not crypto_value or not seuil_value or not alert_type_value:
            messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs avant d'ajouter une alerte.")
            return

        result=add_alerte(self.current_user[0], crypto_value, seuil_value, alert_type_value)
        match result:
            case 0:
                messagebox.showinfo("Succès","Alerte ajoutée avec succès.")
            case 1:
                messagebox.showerror("Erreur", "la monnaie que vous avez choisie est indisponible")
            case 2:
                messagebox.showerror("Erreur","Cette alerte a deja été créée")
            case _:
                messagebox.showerror("Erreur","Une erreur s'est produite , rééssayez")
    
    def afficher_notification(self, message, duree=3000):
        """Affiche une bannière de notification en haut de la fenêtre Tkinter avec grid."""

        # Création du label de notification
        notif_label = tk.Label(self.root, text=message, bg="yellow", fg="black", font=("Arial", 12, "bold"), pady=5)

        # Placement en haut de la fenêtre avec grid (row=0, column=0, et colonne qui s'étend)
        notif_label.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Supprime la notification après 'duree' millisecondes
        self.root.after(duree, notif_label.destroy)
           
    def send_notification(self,root):
        """Met à jour les cryptos et vérifie les alertes à intervalle régulier."""
        
        if self.current_user:
            cryptos_dans_alertes = collect_alerts(self.current_user[0])
        
            for (cryptomonnaie, price, seuil,alert_type) in cryptos_dans_alertes:
                yes=0
                yes=comparaison_price_seuil(self.current_user[0],cryptomonnaie,seuil,alert_type)
                if yes:
                    self.afficher_notification(f"new notif for {cryptomonnaie} : {alert_type} seuil: {seuil} ")

        # Relancer la vérification toutes les heures
        root.after(30000, lambda: self.send_notification(root))

        
if __name__ == "__main__":
    
    init_db()
    root = tk.Tk()
    root.title("Application Crypto")
    
    update_database(root)
    
    frame_tableau = tk.Frame(root) 
    frame_tableau.pack(pady=20)
    
    # 🔹 Initialisation de l'interface
    app = CryptoApp(root)
    app.send_notification(root)



    # Lancement du processus de mise à jour sans bloquer l'UI
    # root.after(5000, lambda: verifier_alertes(root))  # Passer root en argument

    root.mainloop()



    

