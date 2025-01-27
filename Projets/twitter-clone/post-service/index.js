const express = require('express');
const cors = require('cors');
const axios = require('axios');
const app = express();
app.use(cors());
app.use(express.json());

const CACHE_SERVICE_URL = 'http://localhost:3003/cache/posts';
const DB_SERVICE_URL = 'http://localhost:3004/db/posts';

// Endpoint pour publier un message
app.post('/post', async (req, res) => {
    const { pseudo, message } = req.body;
    if (!pseudo || !message) return res.status(400).json({ error: 'Pseudo and message are required' });

    try {
        await axios.post(CACHE_SERVICE_URL, { pseudo, message });
        await axios.post(DB_SERVICE_URL, { pseudo, message });
        res.json({ success: true });
    } catch (err) {
        res.status(500).json({ error: 'Failed to post message' });
    }
});

// Endpoint pour récupérer les messages
app.get('/posts', async (req, res) => {
    try {
        const response = await axios.get(CACHE_SERVICE_URL);
        res.json(response.data);
    } catch (err) {
        res.status(500).json({ error: 'Failed to fetch posts' });
    }
});

app.listen(3002, () => console.log('Post Service running on port 3002'));