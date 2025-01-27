const express = require('express');
const cors = require('cors');
const redis = require('redis');
const app = express();
app.use(cors());
app.use(express.json());

// Créez un client Redis
const client = redis.createClient();

// Gestion des erreurs Redis
client.on('error', (err) => console.error('Redis error:', err));

// Attendez que le client soit connecté avant d'utiliser les méthodes Redis
client.connect().then(() => {
    console.log('Connected to Redis');
}).catch((err) => {
    console.error('Failed to connect to Redis:', err);
});

// Endpoint pour récupérer les messages depuis Redis
app.get('/cache/posts', async (req, res) => {
    try {
        const data = await client.lRange('posts', 0, -1); // Utilisez lRange au lieu de lrange
        res.json(data.map(JSON.parse));
    } catch (err) {
        console.error('Failed to fetch posts from Redis:', err);
        res.status(500).json({ error: 'Failed to fetch posts from Redis' });
    }
});

// Endpoint pour stocker un message dans Redis
app.post('/cache/posts', async (req, res) => {
    const { pseudo, message } = req.body;
    if (!pseudo || !message) return res.status(400).json({ error: 'Pseudo and message are required' });

    try {
        await client.rPush('posts', JSON.stringify({ pseudo, message })); // Utilisez rPush au lieu de rpush
        res.json({ success: true });
    } catch (err) {
        console.error('Failed to store post in Redis:', err);
        res.status(500).json({ error: 'Failed to store post in Redis' });
    }
});

app.listen(3003, () => console.log('Cache Service running on port 3003'));