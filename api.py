
import requests

# api_key='93e5a955-a5ba-4096-9f77-6e0cbd57ec7a'
api_key = '95c095f8-b837-4f71-93e6-b33f4800b59b'

class Crypto:
    def __init__(self, nom, price):
        self.nom = nom
        self.price = price

    
def get_info(cryptomonnaie_name):
    """Crée un objet Crypto en récupérant le prix et la date/heure du dernier trade depuis l'API."""
    headers = {
        'X-CoinAPI-Key': api_key
    }
    url = f'https://rest.coinapi.io/v1/quotes/{cryptomonnaie_name}/current'
    response = requests.get(url, headers=headers)

    # Vérifie si la requête a réussi
    if response.status_code != 200:
        print(f"Erreur : {response.status_code}, {response.text}")
        return None

    # Parse les données de la réponse
    data = response.json()

    # Récupère les informations sur le dernier trade
    last_trade = data.get('last_trade', {})
    if last_trade:
        price = last_trade.get('price', None)
        return Crypto(cryptomonnaie_name,price)

    print("Pas de 'last_trade' trouvé.")
    return None



def get_valid_coinapi_symbols():
    """
    Récupère uniquement les symboles utilisables dans CoinAPI.
    Teste chaque symbole pour voir s'il est valide.
    """
    url = "https://rest.coinapi.io/v1/symbols"
    headers = {
        'X-CoinAPI-Key': api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Liste de symboles filtrés
        valid_symbols = []
        
        for symbol in data:
            symbol_id = symbol["symbol_id"]
            
            # Vérifier que le symbole est bien un marché au comptant ("SPOT")
            if "SPOT" in symbol_id:
                # Vérifier si l'API accepte ce symbole
                if check_symbol_validity(symbol_id, headers):
                    valid_symbols.append(symbol_id)

        return sorted(set(valid_symbols))  # Supprimer doublons et trier

    except requests.exceptions.RequestException as e:
        print(f"Erreur : {e}")
        return []

def check_symbol_validity(symbol_id, headers):
    """
    Vérifie si un symbole est utilisable en testant une requête dessus.
    """
    url = f"https://rest.coinapi.io/v1/quotes/{symbol_id}/current"
    headers = {
        'X-CoinAPI-Key': api_key
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return True  # Le symbole est valide
    except requests.exceptions.RequestException:
        pass
    
    return False  # Le symbole est invalide
