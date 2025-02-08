
import requests
from  classuseful import Crypto

api_key = '5aa6d3a9-cf98-410a-9e26-11c089a24aaf'

# Fonction pour récupérer les informations de prix
def get_info(cryptomonnaie_name):
    """crée un objet Crypto pour recup de l'api le prix de la monnaie passé en parametre """
    headers = {
        'X-CoinAPI-Key': api_key  # Header pour l'authentification
    }
    url = f'https://rest.coinapi.io/v1/quotes/{cryptomonnaie_name}/current'
    response = requests.get(url, headers=headers)  # Utilisation des headers
    
    # Vérifie si la requête a réussi
    if response.status_code != 200:
        print(f"Erreur : {response.status_code}, {response.text}")
        return None
    
    # Parse les données de la réponse
    data = response.json()
    
    # Récupère les informations sur le dernier trade
    last_trade = data.get('last_trade', {})
    if last_trade:
        price = last_trade.get('price', '')
        return Crypto(cryptomonnaie_name, price )
    
    print("Pas de 'last_trade' trouvé.")
    return None

#recup la liste des cryptosmonnaies
def api_get_supported_cryptos():
    """
    Récupère la liste des symboles de trading supportés par l'API CoinAPI.
    """
    url = "https://rest.coinapi.io/v1/symbols"
    headers = {"X-CoinAPI-Key": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lève une erreur si la requête échoue
        data = response.json()

        # Filtrer pour ne garder que les symboles au format KRAKEN_SPOT_BTC_USDT
        symbols = [symbol["symbol_id"] for symbol in data if "SPOT" in symbol["symbol_id"]]

        return symbols

    except requests.exceptions.RequestException:
        return []
