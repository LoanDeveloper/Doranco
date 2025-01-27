const redis = require('redis');
const client = redis.createClient();

client.connect().catch(console.error); // Connexion explicite au client Redis

const express = require('express');
const app = express();

// Simuler une requête à la base de données
function fetchDataFromDB(callback) {
  setTimeout(() => {
    callback("Données récupérées de la base de données");
  }, 2000);
}

app.get('/data', async (req, res) => {
  const cacheKey = 'my_data_cache';

  try {
    // Vérifier si les données sont déjà en cache
    const cachedData = await client.get(cacheKey);
    if (cachedData) {
      return res.send(cachedData); // Renvoie les données depuis le cache
    }

    // Sinon, récupère les données depuis la base de données et les met en cache
    fetchDataFromDB(async (dataFromDB) => {
      await client.setEx(cacheKey, 3600, dataFromDB); // Mise en cache pour 1 heure
      res.send(dataFromDB);
    });
  } catch (err) {
    console.error("Erreur Redis :", err);
    res.status(500).send("Erreur interne du serveur");
  }
});

app.listen(3000, () => {
  console.log('Serveur en écoute sur le port 3000');
});
