import requests
import pymongo
import time
from typing import List

# Configuration de MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "tp_api"
COLLECTION_NAME = "data"

# Connexion à MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def fetch_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 10, "page": 1}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        extracted_data = [{
            "id": item["id"],
            "name": item["name"],
            "symbol": item["symbol"],
            "current_price": item["current_price"],
            "market_cap": item["market_cap"]
        } for item in data]
        
        collection.insert_many(extracted_data)
        print("✅ Données insérées avec succès dans MongoDB.")
    else:
        print("❌ Échec de la récupération des données.")

def get_data():
    return list(collection.find({}, {"_id": 0}))

# Binary Search

def binary_search(data: List[dict], key: str, target):
    left, right = 0, len(data) - 1
    while left <= right:
        mid = (left + right) // 2
        if data[mid][key] == target:
            return mid
        elif data[mid][key] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def linear_search(data: List[dict], key: str, target):
    for i, item in enumerate(data):
        if item[key] == target:
            return i
    return -1

def measure_time_search(search_function, data, key, target):
    start_time = time.time()
    index = search_function(data, key, target)
    end_time = time.time()
    return index, (end_time - start_time) * 1000

def main():
    fetch_data()
    data = get_data()
    key = "current_price"
    data.sort(key=lambda x: x[key])  # Tri pour Binary Search
    
    print("🔍 Recherche d'une valeur avec Binary Search et Linear Search")
    target = float(input("Entrez la valeur de " + key + " à rechercher : "))
    
    binary_index, binary_time = measure_time_search(binary_search, data, key, target)
    linear_index, linear_time = measure_time_search(linear_search, data, key, target)
    
    if binary_index != -1:
        print(f"✅ Binary Search : élément trouvé à l'index {binary_index} en {binary_time:.2f} ms")
    else:
        print("❌ Binary Search : élément non trouvé.")
    
    if linear_index != -1:
        print(f"✅ Linear Search : élément trouvé à l'index {linear_index} en {linear_time:.2f} ms")
    else:
        print("❌ Linear Search : élément non trouvé.")
    
    print(f"🏆 Algorithme le plus rapide : {'Binary Search' if binary_time < linear_time else 'Linear Search'}")
    
if __name__ == "__main__":
    main()
