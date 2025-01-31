from api import *
from datetime import datetime
import bcrypt


def init_db():
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    
    # Créer la table users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Créer la table Cryptomonnaies
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cryptomonnaies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptomonnaie TEXT UNIQUE NOT NULL,
            prix REAL NOT NULL
        )
    """)

    # Créer la table Alertes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alertes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto_id INTEGER NOT NULL,
            seuil REAL NOT NULL,
            FOREIGN KEY (crypto_id) REFERENCES Cryptomonnaies(id) ON DELETE CASCADE
        )
    """)

    # Créer la table Notifications
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto_id INTEGER NOT NULL,
            type_alerte TEXT NOT NULL, 
            FOREIGN KEY (crypto_id) REFERENCES Cryptomonnaies(id) ON DELETE CASCADE
        )
    """)
    
    #créer la table pour suivre le dernier statut de chaque cryptomonnaie par rapport au seuil
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DernieresNotifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto_id INTEGER NOT NULL UNIQUE, 
            dernier_statut TEXT NOT NULL CHECK(dernier_statut IN ('au-dessus', 'en-dessous')),
            date_notif TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (crypto_id) REFERENCES Cryptomonnaies(id) ON DELETE CASCADE
        );
    """)
    connection.commit()
    connection.close()

   
#/---------------------------/
#      table users
#/---------------------------/   
    

def add_user(email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
        connection.commit()
    finally:
        connection.close()

def get_user(email):
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    connection.close()
    return user
    
#/---------------------------/
#      table Crypto 
#/---------------------------/

def add_crypto(nom_crypto, prix):
    """
    Ajoute une nouvelle cryptomonnaie dans la base de données si elle n'existe pas déjà.
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Vérifier si la cryptomonnaie existe déjà
        cursor.execute("SELECT id FROM Cryptomonnaies WHERE cryptomonnaie = ?", (nom_crypto,))
        if cursor.fetchone():
            print(f"La cryptomonnaie {nom_crypto} existe déjà dans la base.")
            return

        # Ajouter la cryptomonnaie
        cursor.execute("""
            INSERT INTO Cryptomonnaies (cryptomonnaie, prix)
            VALUES (?, ?)
        """, (nom_crypto, prix))

        connection.commit()
        print(f" {nom_crypto} ajoutée avec un prix de {prix}.")

    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de {nom_crypto} : {e}")
    
    finally:
        connection.close()

def update_crypto():
    """
    Met à jour les prix des cryptos existantes et ajoute celles qui ne sont pas encore dans la base.
    """
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()

    # Récupérer toutes les cryptos enregistrées dans la base
    cursor.execute("SELECT cryptomonnaie, prix FROM Cryptomonnaies")
    cryptos_db = {nom: prix for nom, prix in cursor.fetchall()}  # Dictionnaire {nom_crypto: prix}

    # Récupérer la liste des cryptos que l'API prend en charge
    liste_cryptos_api = ['OKCOINUSD_SPOT_BTC_USD', 'COINBASE_SPOT_BTC_USD']

    for nom_crypto in liste_cryptos_api:
        
        crypto_api =get_info(nom_crypto)  # Retourne un objet Crypto(nom, prix)

        if nom_crypto in cryptos_db:
            prix_db = cryptos_db[nom_crypto]

            # Vérifier si le prix a changé
            if crypto_api.prix != prix_db:

                cursor.execute("""
                    UPDATE Cryptomonnaies
                    SET prix = ?
                    WHERE cryptomonnaie = ?
                """, (crypto_api.prix, nom_crypto))
        else:
            
            # Ajouter la nouvelle crypto à la base
            if crypto_api is not None:
                add_crypto(nom_crypto, crypto_api.prix)
            else:
                print(f"Erreur : Impossible de récupérer les données pour {nom_crypto}")


    connection.commit()
    connection.close()
    
    
def delete_crypto(monnaie, seuil):
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM crypto WHERE monnaie = ? AND seuil = ?", (monnaie, seuil))
    connection.commit()
    connection.close()
    
#/---------------------------/
#      table Alerte
#/-------------------- Assurer que chaque crypto_id est unique---------/
      
def add_alerte(crypto, seuil):
    
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        #obtenir id crytomonnaie
        cursor.execute("SELECT id FROM Cryptomonnaies WHERE cryptomonnaie = ?", (crypto,))
        crypto_id = cursor.fetchone()

        # Vérifier si l'alerte existe déjà pour cette cryptomonnaie et seuil
        cursor.execute("SELECT id FROM Alertes WHERE crypto_id = ? AND seuil = ?", (crypto_id[0], seuil))
        if cursor.fetchone():
            return 

        # Ajouter l'alerte
        cursor.execute("INSERT INTO Alertes (crypto_id, seuil) VALUES (?, ?)", (crypto_id[0], seuil))
        connection.commit()
        print(f" Alerte ajoutée pour {crypto} au seuil {seuil}.")

        connection.close()

        
def delete_alerte(crypto,seuil):
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Vérifier si l'alerte existe
        cursor.execute("SELECT id FROM Alertes WHERE crypto_id = ? AND seuil = ?",
                       (crypto, seuil))
        if cursor.fetchone() is None:
            print(f"Aucune alerte trouvée pour {crypto}.")
            return

        # Supprimer l'alerte
        cursor.execute("DELETE FROM Alertes WHERE crypto = ?", (crypto,))
        connection.commit()
        print(f"Alerte supprimée pour {crypto}.")

    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de l'alerte : {e}")
    
    finally:
        connection.close()

import sqlite3

def get_monnaies_avec_alertes():
    """ Récupérer tous les résultats sous forme de tuples (cryptomonnaie, prix, seuil)"""
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT Cryptomonnaies.cryptomonnaie, Cryptomonnaies.prix, Alertes.seuil 
            FROM Alertes 
            JOIN Cryptomonnaies ON Alertes.crypto_id = Cryptomonnaies.id
        """)
  
        resultats = cursor.fetchall()
        
        print("Liste des monnaies avec prix et alertes:", resultats)
        return resultats
        
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des alertes: {e}")
        return []
    finally:
        connection.close()
        

def comparaison_prix_seuil(cryptomonnaie, prix:float, seuil:float):
    """Compare le prix d'une cryptomonnaie et le seuil défini par l'utilisateur et crée une notification si nécessaire"""
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Récupérer l'ID de la cryptomonnaie
        cursor.execute("SELECT id FROM Cryptomonnaies WHERE cryptomonnaie = ?", (cryptomonnaie,))
        crypto_id = cursor.fetchone()
        if not crypto_id:
            print(f"Crypto {cryptomonnaie} introuvable.")
            return
        crypto_id = crypto_id[0]

        # Récupérer le dernier statut enregistré
        cursor.execute("SELECT dernier_statut FROM DernieresNotifications WHERE crypto_id = ?", (crypto_id,))
        dernier_statut = cursor.fetchone()

        # Déterminer le nouveau statut
        if prix > seuil:
            nouveau_statut = "au-dessus"
            message = f"{cryptomonnaie} est monté au-dessus du seuil : {seuil}"
        else:
            nouveau_statut = "en-dessous"
            message = f"{cryptomonnaie} est passé sous le seuil : {seuil}"

        # Vérifier si le statut a changé
        if not dernier_statut or dernier_statut[0] != nouveau_statut:
            add_notification(cryptomonnaie, seuil, message) 
            
            # Mettre à jour ou insérer le nouveau statut dans DernieresNotifications
            cursor.execute("""
                INSERT INTO DernieresNotifications (crypto_id, dernier_statut, date_notif) 
                VALUES (?, ?, ?)
                ON CONFLICT(crypto_id) DO UPDATE SET dernier_statut = excluded.dernier_statut, date_notif = excluded.date_notif
            """, (crypto_id, nouveau_statut, datetime.now()))

            connection.commit()

    except sqlite3.Error as e:
        print(f" Erreur lors de la comparaison du prix et du seuil : {e}")
    
    finally:
        connection.close()
        
        
def verifier_alertes(root):
    """Met à jour les cryptos et vérifie les alertes à intervalle régulier."""
    update_crypto()
    cryptos_dans_alertes = get_monnaies_avec_alertes()
    
    for (cryptomonnaie, prix, seuil) in cryptos_dans_alertes:
        comparaison_prix_seuil(cryptomonnaie, float(prix), float(seuil))

    #Relancer la vérification toutes les 60 secondes
    root.after(60000, lambda: verifier_alertes(root))

    
# /**********************************/



#/---------------------------/
#      table notif
#/---------------------------/


def add_notification(crypto, seuil, changement):
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()


        # Ajouter la notification dans la table Notifications
        cursor.execute("""
            INSERT INTO Notifications (crypto_id, seuil, type_alerte) 
            VALUES ((SELECT id FROM Cryptomonnaies WHERE cryptomonnaie = ?), ?, ?)
        """, (crypto, seuil, changement))

        # Envoyer la notification (fonction send_notif doit être définie ailleurs)
        send_notif(f"{crypto} {changement} le seuil de {seuil}€")

        connection.commit()
        print(f" Notification ajoutée : {crypto} a {changement} le seuil de {seuil}.")

    except sqlite3.Error as e:
        print(f" Erreur lors de l'ajout de la notification : {e}")

    finally:
        connection.close()



def delete_notification(crypto):
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Vérifier si la notification existe
        cursor.execute("SELECT id FROM Notifications WHERE crypto = ?", (crypto,))
        if cursor.fetchone() is None:
            print(f"Aucune notification trouvée pour {crypto}.")
            return

        # Supprimer la notification
        cursor.execute("DELETE FROM Notifications WHERE crypto = ?", (crypto,))
        connection.commit()
        print(f"Notification supprimée pour {crypto}.")

    except sqlite3.Error as e:
        print(f" Erreur lors de la suppression de la notification : {e}")
    
    finally:
        connection.close()
        

def get_historique_notifications():
    """Récupère l'historique des dernières notifications envoyées."""
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT Cryptomonnaies.cryptomonnaie, DernieresNotifications.dernier_statut, DernieresNotifications.date_notif
            FROM DernieresNotifications
            JOIN Cryptomonnaies ON DernieresNotifications.crypto_id = Cryptomonnaies.id
            ORDER BY DernieresNotifications.date_notif DESC
        """)
        
        notifications = cursor.fetchall()
        
        print("Historique des dernières notifications :")
        for crypto, statut, date in notifications:
            print(f"- {crypto} : {statut} (Envoyé le {date})")

        return notifications

    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des notifications : {e}")
        return []
    
    finally:
        connection.close()
        
def send_notif(crypto,changement,seuil):
    return 



        


