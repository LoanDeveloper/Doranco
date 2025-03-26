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

# Algorithmes de tri
def bubble_sort(data: List[dict], key: str):
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j][key] > arr[j+1][key]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def selection_sort(data: List[dict], key: str):
    arr = data.copy()
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j][key] < arr[min_idx][key]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insertion_sort(data: List[dict], key: str):
    arr = data.copy()
    for i in range(1, len(arr)):
        key_item = arr[i]
        j = i - 1
        while j >= 0 and key_item[key] < arr[j][key]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_item
    return arr

def quick_sort(data: List[dict], key: str):
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2]
    left = [x for x in data if x[key] < pivot[key]]
    middle = [x for x in data if x[key] == pivot[key]]
    right = [x for x in data if x[key] > pivot[key]]
    return quick_sort(left, key) + middle + quick_sort(right, key)

def measure_time(sort_function, data, key):
    start_time = time.time()
    sorted_data = sort_function(data, key)
    end_time = time.time()
    return sorted_data, (end_time - start_time) * 1000

def main():
    fetch_data()
    data = get_data()
    key = "current_price"
    
    print("🔍 Mesure des performances des tris sur", key)
    
    results = {
        "Bubble Sort": measure_time(bubble_sort, data, key),
        "Selection Sort": measure_time(selection_sort, data, key),
        "Insertion Sort": measure_time(insertion_sort, data, key),
        "Quick Sort": measure_time(quick_sort, data, key)
    }
    
    for algo, (sorted_data, time_taken) in results.items():
        print(f"{algo}: {time_taken:.2f} ms")
    
    best_algo = min(results, key=lambda k: results[k][1])
    print(f"🏆 Algorithme le plus rapide : {best_algo} ({results[best_algo][1]:.2f} ms)")
    
    print("📊 Données triées avec l'algorithme optimal:")
    for item in results[best_algo][0]:
        print(item)

if __name__ == "__main__":
    main()
