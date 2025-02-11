from api import supported_crypto, get_info
import bcrypt
import sqlite3



def init_db():
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    
    #user_table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username STRING NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    #Cryptomonnaie_table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cryptocurrency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptomonnaie TEXT UNIQUE NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Alerts_table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alertes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            crypto_id INTEGER NOT NULL,
            seuil REAL NOT NULL,
            alert_type TEXT NOT NULL,
            FOREIGN KEY (crypto_id) REFERENCES Cryptocurrency(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
        )
    """)

    #history_table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HistoriqueNotifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,  
            FOREIGN KEY (crypto_id) REFERENCES Cryptocurrency(id) ON DELETE CASCADE
        );
    """)

    connection.commit()
    connection.close()

   
#/---------------------------/
#      table Users
#/---------------------------/   

def add_user(username, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Users(username, email, password) VALUES (?, ?, ?)", 
                       (username, email, hashed_password))
        connection.commit()
    finally:
        connection.close()

def get_user(email):
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()
    connection.close()
    return user
    
#/---------------------------/
#      table Crypto 
#/---------------------------/

def add_crypto(nom_crypto, price):
    """
    Ajoute une nouvelle cryptomonnaie dans la base de données si elle n'existe pas déjà.
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Vérifier si la cryptomonnaie existe déjà
        cursor.execute("SELECT id FROM Cryptocurrency WHERE cryptomonnaie = ?", (nom_crypto,))
        if cursor.fetchone():
            print(f"La cryptomonnaie {nom_crypto} existe déjà dans la base.")
            connection.close()
            return

        # Ajouter la cryptomonnaie
        cursor.execute("""
            INSERT INTO Cryptocurrency (cryptomonnaie, price)
            VALUES (?, ?)
        """, (nom_crypto, price))

        connection.commit()
        print(f"{nom_crypto} ajoutée avec un prix de {price}.")

    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de {nom_crypto} : {e}")
    
    finally:
        connection.close()

def delete_crypto(nom_crypto):
    """
    Supprime une cryptomonnaie de la base de données.
    """
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Cryptocurrency WHERE cryptomonnaie = ?", (nom_crypto,))
    connection.commit()
    connection.close()
    print(f"{nom_crypto} supprimée de la base.")
    
    
def collect_crypto_list():
    """Récupère la liste des noms des Cryptocurrency depuis la base de données."""
    try:
        with sqlite3.connect("crypto_app.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT cryptomonnaie FROM Cryptocurrency")
            return [nom for (nom,) in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des Cryptocurrency : {e}")
        return []
    finally:
        connection.close()    

def update_crypto():
    """
    Met à jour la base de données des cryptos :
    - Ajoute celles qui n'existent pas encore.
    - Met à jour le prix des cryptos existantes.
    - Supprime celles qui ne figurent plus dans l'API.
    """
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()

    # Récupérer toutes les cryptos enregistrées dans la base
    cursor.execute("SELECT cryptomonnaie FROM Cryptocurrency")
    cryptos_db = {nom for nom, in cursor.fetchall()}  # Set des cryptos en base

    # Cryptos à ajouter
    for nom_crypto in supported_crypto:
        crypto_api = get_info(nom_crypto)  # Objet Crypto(nom, price)

        if nom_crypto in cryptos_db:
            # Mettre à jour le prix si nécessaire
            cursor.execute("SELECT price FROM Cryptocurrency WHERE cryptomonnaie = ?", (nom_crypto,))
            price_db = cursor.fetchone()[0]

            if crypto_api and crypto_api.price != price_db:
                cursor.execute("UPDATE Cryptocurrency SET price = ? WHERE cryptomonnaie = ?", (crypto_api.price, nom_crypto))
                print(f"{nom_crypto} mis à jour avec un prix de {crypto_api.price}.")
        else:
            # Ajouter la nouvelle crypto
            if crypto_api:
                add_crypto(nom_crypto, crypto_api.price)
    connection.commit()
    connection.close()
    
    # Cryptos à supprimer
    cryptos_to_delete = cryptos_db - set(supported_crypto)
    for crypto in cryptos_to_delete:
        delete_crypto(crypto)
    
    print("Mise à jour terminée.")


from api import supported_crypto, get_info
import bcrypt
import sqlite3



def init_db():
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    
    #user_table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username STRING NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    #Cryptomonnaie_table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cryptocurrency (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cryptomonnaie TEXT UNIQUE NOT NULL,
            price REAL NOT NULL
        )
    """)

    # Alerts_table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alertes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            crypto_id INTEGER NOT NULL,
            seuil REAL NOT NULL,
            alert_type TEXT NOT NULL,
            FOREIGN KEY (crypto_id) REFERENCES Cryptocurrency(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
        )
    """)

    #history_table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS HistoriqueNotifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crypto_id INTEGER NOT NULL,
            timestamp TEXT NOT NULL,  
            FOREIGN KEY (crypto_id) REFERENCES Cryptocurrency(id) ON DELETE CASCADE
        );
    """)

    connection.commit()
    connection.close()

   
#/---------------------------/
#      table Users
#/---------------------------/   

def add_user(username, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Users(username, email, password) VALUES (?, ?, ?)", 
                       (username, email, hashed_password))
        connection.commit()
    finally:
        connection.close()

def get_user(email):
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE email = ?", (email,))
    user = cursor.fetchone()
    connection.close()
    return user
    
#/---------------------------/
#      table Crypto 
#/---------------------------/

def add_crypto(nom_crypto, price):
    """
    Ajoute une nouvelle cryptomonnaie dans la base de données si elle n'existe pas déjà.
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Vérifier si la cryptomonnaie existe déjà
        cursor.execute("SELECT id FROM Cryptocurrency WHERE cryptomonnaie = ?", (nom_crypto,))
        if cursor.fetchone():
            print(f"La cryptomonnaie {nom_crypto} existe déjà dans la base.")
            connection.close()
            return

        # Ajouter la cryptomonnaie
        cursor.execute("""
            INSERT INTO Cryptocurrency (cryptomonnaie, price)
            VALUES (?, ?)
        """, (nom_crypto, price))

        connection.commit()
        print(f"{nom_crypto} ajoutée avec un prix de {price}.")

    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de {nom_crypto} : {e}")
    
    finally:
        connection.close()

def delete_crypto(nom_crypto):
    """
    Supprime une cryptomonnaie de la base de données.
    """
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Cryptocurrency WHERE cryptomonnaie = ?", (nom_crypto,))
    connection.commit()
    connection.close()
    print(f"{nom_crypto} supprimée de la base.")
    
    
def collect_crypto_list():
    """Récupère la liste des noms des Cryptocurrency depuis la base de données."""
    try:
        with sqlite3.connect("crypto_app.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT cryptomonnaie FROM Cryptocurrency")
            return [nom for (nom,) in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des Cryptocurrency : {e}")
        return []
    finally:
        connection.close()    

def update_crypto():
    """
    Met à jour la base de données des cryptos :
    - Ajoute celles qui n'existent pas encore.
    - Met à jour le prix des cryptos existantes.
    - Supprime celles qui ne figurent plus dans l'API.
    """
    connection = sqlite3.connect("crypto_app.db")
    cursor = connection.cursor()

    # Récupérer toutes les cryptos enregistrées dans la base
    cursor.execute("SELECT cryptomonnaie FROM Cryptocurrency")
    cryptos_db = {nom for nom, in cursor.fetchall()}  # Set des cryptos en base

    # Cryptos à ajouter
    for nom_crypto in supported_crypto:
        crypto_api = get_info(nom_crypto)  # Objet Crypto(nom, price)

        if nom_crypto in cryptos_db:
            # Mettre à jour le prix si nécessaire
            cursor.execute("SELECT price FROM Cryptocurrency WHERE cryptomonnaie = ?", (nom_crypto,))
            price_db = cursor.fetchone()[0]

            if crypto_api and crypto_api.price != price_db:
                cursor.execute("UPDATE Cryptocurrency SET price = ? WHERE cryptomonnaie = ?", (crypto_api.price, nom_crypto))
                print(f"{nom_crypto} mis à jour avec un prix de {crypto_api.price}.")
        else:
            # Ajouter la nouvelle crypto
            if crypto_api:
                add_crypto(nom_crypto, crypto_api.price)
    connection.commit()
    connection.close()
    
    # Cryptos à supprimer
    cryptos_to_delete = cryptos_db - set(supported_crypto)
    for crypto in cryptos_to_delete:
        delete_crypto(crypto)
    
    print("Mise à jour terminée.")




    
#/---------------------------/
#      table Alerte
#/-----------------------------/
      

def add_alerte(user_id, crypto, seuil, alert_type):
    """
    Ajoute une alerte pour une cryptomonnaie donnée.
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Obtenir l'ID de la cryptomonnaie
        cursor.execute("SELECT id FROM Cryptocurrency WHERE cryptomonnaie = ?", (crypto,))
        crypto_id = cursor.fetchone()

        if not crypto_id:
            print(f"La cryptomonnaie {crypto} n'existe pas dans la base.")
            return 1

        crypto_id = crypto_id[0]

        # Vérifier si l'alerte existe déjà
        cursor.execute("""
            SELECT id FROM Alertes 
            WHERE user_id = ? AND crypto_id = ? AND seuil = ? AND alert_type = ?
        """, (user_id, crypto_id, seuil, alert_type))

        if cursor.fetchone():
            print(f"Une alerte pour {crypto} au seuil {seuil} existe déjà.")
            return 2

        # Ajouter l'alerte
        cursor.execute("""
            INSERT INTO Alertes (user_id, crypto_id, seuil, alert_type) 
            VALUES (?, ?, ?, ?)
        """, (user_id, crypto_id, seuil, alert_type))

        connection.commit()
        print(f"Alerte ajoutée pour {crypto} au seuil {seuil}.")
        return 0

    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de l'alerte : {e}")
        return 3

    finally:
        connection.close()


def delete_alerte(user_id, crypto, seuil,alert_type):
    """
    Supprime une alerte spécifique d'un utilisateur pour une cryptomonnaie donnée.
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Obtenir l'ID de la cryptomonnaie
        cursor.execute("SELECT id FROM Cryptocurrency WHERE cryptomonnaie = ?", (crypto,))
        crypto_id = cursor.fetchone()

        if not crypto_id:
            print(f"La cryptomonnaie {crypto} n'existe pas dans la base.")
            return

        crypto_id = crypto_id[0]

        # Vérifier si l'alerte existe
        cursor.execute("""
            SELECT id FROM Alertes 
            WHERE user_id = ? AND crypto_id = ? AND seuil = ? AND alert_type= ?
        """, (user_id, crypto_id, seuil,alert_type))

        if cursor.fetchone() is None:
            print(f"Aucune alerte trouvée pour {crypto} au seuil {seuil} et type {alert_type}.")
            return

        # Supprimer l'alerte
        cursor.execute("""
            DELETE FROM Alertes 
            WHERE user_id = ? AND crypto_id = ? AND seuil = ? AND alert_type= ?
        """, (user_id, crypto_id, seuil, alert_type))

        connection.commit()
        print(f"Alerte supprimée pour {crypto} au seuil {seuil} et type {alert_type}")

    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de l'alerte : {e}")

    finally:
        connection.close()


def collect_alerts(user_id):
    """
    Récupère toutes les Cryptocurrency ayant des alertes pour un utilisateur donné.
    Retourne une liste de tuples (cryptomonnaie, price, seuil, alert_type).
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT Cryptocurrency.cryptomonnaie, Cryptocurrency.price, Alertes.seuil, Alertes.alert_type
            FROM Alertes
            JOIN Cryptocurrency ON Alertes.crypto_id = Cryptocurrency.id
            WHERE Alertes.user_id = ?;
        """, (user_id,))

        resultats = cursor.fetchall()

        print(f" Liste des cryptos avec alertes pour l'utilisateur {user_id} : {resultats}")
        return resultats

    except sqlite3.Error as e:
        print(f"  Erreur lors de la récupération des alertes : {e}")
        return []

    finally:
        connection.close()


def comparaison_price_seuil(user_id,crypto,seuil,alert_type):
    """Compare le prix des Cryptocurrency avec leur seuil et affiche une notification si nécessaire"""
    try:
        
        connection = sqlite3.connect("crypto_app.db")
        
        cursor = connection.cursor()
        
        # get the current price of crypto
        cursor.execute("SELECT price FROM Cryptocurrency WHERE cryptomonnaie = ?", (crypto,))
        crypto_price= cursor.fetchone()
        if not crypto_price:
            print(f" La cryptomonnaie {crypto} n'existe pas dans la base.")
            return
        crypto_price = crypto_price[0]
        
        if (crypto_price<seuil and alert_type=="Au-dessous"):
            print("il faut envoyer notif")
            return 1
        if (crypto_price>seuil and alert_type=="Au-dessus"):
            print("il faut envoyer notif")
            return 1
        if (crypto_price==seuil and alert_type=="Égal"):
            print("il faut envoyer notif")
            return 1
        else:
            print("pas de notif en vue")
            return 0
            

    except Exception as e:
        print(f"Erreur lors de la comparaison des prix et seuils : {e}")



def update_database(root):
    update_crypto()
    #rajouter l'update de l'historique 
    #lancer en crontab

    
#/---------------------------/
#      table Alerte
#/-----------------------------/
      

def add_alerte(user_id, crypto, seuil, alert_type):
    """
    Ajoute une alerte pour une cryptomonnaie donnée.
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Obtenir l'ID de la cryptomonnaie
        cursor.execute("SELECT id FROM Cryptocurrency WHERE cryptomonnaie = ?", (crypto,))
        crypto_id = cursor.fetchone()

        if not crypto_id:
            print(f"La cryptomonnaie {crypto} n'existe pas dans la base.")
            return 1

        crypto_id = crypto_id[0]

        # Vérifier si l'alerte existe déjà
        cursor.execute("""
            SELECT id FROM Alertes 
            WHERE user_id = ? AND crypto_id = ? AND seuil = ? AND alert_type = ?
        """, (user_id, crypto_id, seuil, alert_type))

        if cursor.fetchone():
            print(f"Une alerte pour {crypto} au seuil {seuil} existe déjà.")
            return 2

        # Ajouter l'alerte
        cursor.execute("""
            INSERT INTO Alertes (user_id, crypto_id, seuil, alert_type) 
            VALUES (?, ?, ?, ?)
        """, (user_id, crypto_id, seuil, alert_type))

        connection.commit()
        print(f"Alerte ajoutée pour {crypto} au seuil {seuil}.")
        return 0

    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de l'alerte : {e}")
        return 3

    finally:
        connection.close()


def delete_alerte(user_id, crypto, seuil,alert_type):
    """
    Supprime une alerte spécifique d'un utilisateur pour une cryptomonnaie donnée.
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        # Obtenir l'ID de la cryptomonnaie
        cursor.execute("SELECT id FROM Cryptocurrency WHERE cryptomonnaie = ?", (crypto,))
        crypto_id = cursor.fetchone()

        if not crypto_id:
            print(f" La cryptomonnaie {crypto} n'existe pas dans la base.")
            return

        crypto_id = crypto_id[0]

        # Vérifier si l'alerte existe
        cursor.execute("""
            SELECT id FROM Alertes 
            WHERE user_id = ? AND crypto_id = ? AND seuil = ? AND alert_type= ?
        """, (user_id, crypto_id, seuil,alert_type))

        if cursor.fetchone() is None:
            print(f"Aucune alerte trouvée pour {crypto} au seuil {seuil} et type {alert_type}.")
            return

        # Supprimer l'alerte
        cursor.execute("""
            DELETE FROM Alertes 
            WHERE user_id = ? AND crypto_id = ? AND seuil = ? AND alert_type= ?
        """, (user_id, crypto_id, seuil, alert_type))

        connection.commit()
        print(f"Alerte supprimée pour {crypto} au seuil {seuil} et type {alert_type}")

    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de l'alerte : {e}")

    finally:
        connection.close()


def collect_alerts(user_id):
    """
    Récupère toutes les Cryptocurrency ayant des alertes pour un utilisateur donné.
    Retourne une liste de tuples (cryptomonnaie, price, seuil, alert_type).
    """
    try:
        connection = sqlite3.connect("crypto_app.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT Cryptocurrency.cryptomonnaie, Cryptocurrency.price, Alertes.seuil, Alertes.alert_type
            FROM Alertes
            JOIN Cryptocurrency ON Alertes.crypto_id = Cryptocurrency.id
            WHERE Alertes.user_id = ?;
        """, (user_id,))

        resultats = cursor.fetchall()

        print(f" Liste des cryptos avec alertes pour l'utilisateur {user_id} : {resultats}")
        return resultats

    except sqlite3.Error as e:
        print(f"  Erreur lors de la récupération des alertes : {e}")
        return []

    finally:
        connection.close()


def comparaison_price_seuil(user_id,crypto,seuil,alert_type):
    """Compare le prix des Cryptocurrency avec leur seuil et affiche une notification si nécessaire"""
    try:
        
        connection = sqlite3.connect("crypto_app.db")
        
        cursor = connection.cursor()
        
        # get the current price of crypto
        cursor.execute("SELECT price FROM Cryptocurrency WHERE cryptomonnaie = ?", (crypto,))
        crypto_price= cursor.fetchone()
        if not crypto_price:
            print(f" La cryptomonnaie {crypto} n'existe pas dans la base.")
            return
        crypto_price = crypto_price[0]
        
        if (crypto_price<seuil and alert_type=="Au-dessous"):
            print("il faut envoyer notif")
            return 1
        if (crypto_price>seuil and alert_type=="Au-dessus"):
            print("il faut envoyer notif")
            return 1
        if (crypto_price==seuil and alert_type=="Égal"):
            print("il faut envoyer notif")
            return 1
        else:
            print("pas de notif en vue")
            return 0
            

    except Exception as e:
        print(f"Erreur lors de la comparaison des prix et seuils : {e}")



def update_database(root):
    update_crypto()
    #rajouter l'update de l'historique 
    #lancer en crontab


        


