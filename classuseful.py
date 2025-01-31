# /**************  objets et fonctions utiles ********************/
class Crypto:
    def __init__(self, nom, prix):
        self.nom = nom
        self.prix = prix
        
class Notif:
    def __init__(self, crypto, seuil, type):
        self.crypto = crypto
        self.seuil=seuil
        self.type=type
           
class AlerteExistante(Exception):
    """Exception levée lorsqu'une alerte pour une cryptomonnaie et un seuil donnés existe déjà."""
    def __init__(self, crypto, seuil):
        self.crypto = crypto
        self.seuil = seuil
        super().__init__(f"L'alerte pour {crypto} au seuil {seuil} existe déjà.")
        
    
# /**********************************/