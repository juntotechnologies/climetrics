const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(express.json());

// Serve static files from the React build in the client directory
app.use(express.static(path.join(__dirname, '../build')));

// Basic route
app.get('/api/test', (req, res) => {
  res.json({ message: 'Server is running!' });
});

// Handle React routing, return all requests to React app
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, '../build', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
}); 