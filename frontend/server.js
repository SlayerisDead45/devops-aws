const fetch = (...args) => import('node-fetch').then(({default: f}) => f(...args));
const express = require('express');
const path = require('path');
const app = express();

// this lets express read json data
app.use(express.json());

// serve the html file
app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// form data comes here first, then express sends it to flask
app.post('/submit', async function(req, res) {
    const userText = req.body.content;

    try {
        const response = await fetch(process.env.FLASK_URL + '/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: userText })
        });
        const data = await response.json();
        res.json(data);
    } catch (err) {
        res.json({ status: "error", error_msg: "Could not reach Flask backend" });
    }
});

app.listen(3000, function() {
    console.log("Node frontend server running on port 3000");
});