import requests
from collections import deque

# Configuration de l'API NewsAPI
API_KEY = "90638157696d4629b8ffb14f0e902f45"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + API_KEY

class NewsQueue:
    def __init__(self):
        self.queue = deque()
    
    def enqueue(self, article):
        self.queue.append(article)
    
    def dequeue(self):
        if not self.is_empty():
            return self.queue.popleft()
        return None
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def size(self):
        return len(self.queue)

class NewsStack:
    def __init__(self):
        self.stack = []
    
    def push(self, article):
        self.stack.append(article)
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)

def fetch_news():
    try:
        response = requests.get(NEWS_API_URL)
        if response.status_code == 200:
            data = response.json()
            return [(article["title"], article["url"]) for article in data.get("articles", [])]
        else:
            print("Erreur lors de la récupération des actualités.")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion: {e}")
        return []

def main():
    news_queue = NewsQueue()
    news_stack = NewsStack()
    
    print("Récupération des actualités...")
    articles = fetch_news()
    for article in articles:
        news_queue.enqueue(article)
    
    while True:
        print("\nMenu:")
        print("1. Lire un article")
        print("2. Voir le dernier article lu")
        print("3. Quitter")
        
        choix = input("Choisissez une option: ")
        
        if choix == "1":
            if not news_queue.is_empty():
                article = news_queue.dequeue()
                news_stack.push(article)
                print(f"\nTitre: {article[0]}\nURL: {article[1]}\n")
            else:
                print("Aucun article en attente.")
        elif choix == "2":
            if not news_stack.is_empty():
                article = news_stack.pop()
                print(f"\nDernier article lu:\nTitre: {article[0]}\nURL: {article[1]}\n")
            else:
                print("Aucun historique disponible.")
        elif choix == "3":
            print("Fermeture de l'application.")
            break
        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
