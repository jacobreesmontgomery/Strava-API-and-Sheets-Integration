const express = require('express');
const path = require('path');
const axios = require('axios');
const app = express();
const cors = require('cors');
const port = 5001;

// Use CORS middleware for cross-origin requests
app.use(cors());

// Middleware to parse JSON bodies
app.use(express.json());

// Static file serving middleware
const directory = 'C:/Users/17178/Desktop/GITHUB_PROJECTS/Strava-API-and-Sheets-Integration/python/code';
app.use('/files', express.static(directory));

const backendUrl = 'http://localhost:5000';
// Route to handle requests and forward to FastAPI backend
app.get('/api/basic-stats', async (req, res) => {
    try {
        const response = await axios.get(`${backendUrl}/api/basic-stats`);
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).json({
            message: error.message,
        });
    }
});

app.get('/api/database', async (req, res) => {
    try {
        const response = await axios.get(`${backendUrl}/api/database`);
        res.json(response.data);
    } catch (error) {
        res.status(error.response ? error.response.status : 500).json({
            message: error.message,
        });
    }
});

app.get('/api/strava_auth', async (req, res) => {
    console.log('Redirecting to Strava OAuth');
    res.redirect(`${backendUrl}/api/strava_auth`);
})

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
