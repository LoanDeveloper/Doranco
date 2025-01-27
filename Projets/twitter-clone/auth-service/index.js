const express = require('express');
const bodyParser = require('body-parser');
require('dotenv').config(); // Au début de votre fichier index.js
const jwt = require('jsonwebtoken');
const cors = require('cors'); // Importez CORS

const app = express();
app.use(bodyParser.json());
app.use(cors()); // Activez CORS pour toutes les routes


const SECRET_KEY = process.env.SECRET_KEY;
const users = new Map(); // Stockage en mémoire des pseudonymes

// Endpoint pour choisir un pseudonyme
app.post('/auth/choose-pseudo', (req, res) => {
    const { pseudo } = req.body;
    if (!pseudo) return res.status(400).json({ error: 'Pseudo is required' });

    if (users.has(pseudo)) {
        return res.status(400).json({ error: 'Pseudo already taken' });
    }

    const token = jwt.sign({ pseudo }, SECRET_KEY, { expiresIn: '1h' });
    users.set(pseudo, token);
    res.json({ token });
});

// Endpoint pour valider une session
app.get('/auth/validate-session', (req, res) => {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) return res.status(401).json({ error: 'Unauthorized' });

    try {
        const decoded = jwt.verify(token, SECRET_KEY);
        res.json({ pseudo: decoded.pseudo });
    } catch (err) {
        res.status(401).json({ error: 'Invalid token' });
    }
});

app.listen(3001, () => console.log('Auth Service running on port 3001'));