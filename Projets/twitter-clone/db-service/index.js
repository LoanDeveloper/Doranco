const express = require('express');
const cors = require('cors');
const mysql = require('mysql2');
const app = express();
app.use(cors());
app.use(express.json());

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'twitter-clone'
});

connection.connect();

// Endpoint pour récupérer les messages depuis MySQL
app.get('/db/posts', (req, res) => {
    connection.query('SELECT * FROM posts', (err, results) => {
        if (err) return res.status(500).json({ error: 'Failed to fetch posts from MySQL' });
        res.json(results);
    });
});

// Endpoint pour stocker un message dans MySQL
app.post('/db/posts', (req, res) => {
    const { pseudo, message } = req.body;
    if (!pseudo || !message) return res.status(400).json({ error: 'Pseudo and message are required' });

    connection.query('INSERT INTO posts (pseudo, message) VALUES (?, ?)', [pseudo, message], (err) => {
        if (err) return res.status(500).json({ error: 'Failed to store post in MySQL' });
        res.json({ success: true });
    });
});

app.listen(3004, () => console.log('Database Service running on port 3004'));