const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const templatesRouter = require('./routes/templates');
const aiRouter = require('./routes/ai');

const app = express();
const PORT = process.env.PORT || 3001;
const TEMPLATES_DIR = path.join(__dirname, '..', 'templates');
const DB_PATH = path.join(__dirname, '..', 'db.sqlite');

// Ensure templates directory exists
if (!fs.existsSync(TEMPLATES_DIR)) {
  fs.mkdirSync(TEMPLATES_DIR);
}
// Ensure db.sqlite exists (empty file, will be initialized by model)
if (!fs.existsSync(DB_PATH)) {
  fs.writeFileSync(DB_PATH, '');
}

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Static file serving for templates
app.use('/templates', express.static(TEMPLATES_DIR));

// API routes
app.use('/api/templates', templatesRouter);
app.use('/api/ai', aiRouter);

app.get('/', (req, res) => {
  res.send('Local backend for Word Legal Assistant is running.');
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});