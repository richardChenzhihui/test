const path = require('path');
const fs = require('fs');
const sqlite3 = require('sqlite3').verbose();

const DB_PATH = path.join(__dirname, '../../db.sqlite');
const TEMPLATES_DIR = path.join(__dirname, '../../templates');

// 初始化数据库
const db = new sqlite3.Database(DB_PATH);
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    originalname TEXT NOT NULL,
    mimetype TEXT,
    size INTEGER,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
});

exports.getAllTemplates = (req, res) => {
  db.all('SELECT id, originalname, mimetype, size, uploaded_at FROM templates', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
};

exports.uploadTemplate = (req, res) => {
  if (!req.file) return res.status(400).json({ error: 'No file uploaded' });
  const { filename, originalname, mimetype, size } = req.file;
  db.run(
    'INSERT INTO templates (filename, originalname, mimetype, size) VALUES (?, ?, ?, ?)',
    [filename, originalname, mimetype, size],
    function (err) {
      if (err) return res.status(500).json({ error: err.message });
      res.json({ id: this.lastID, originalname, mimetype, size });
    }
  );
};

exports.getTemplateById = (req, res) => {
  const id = req.params.id;
  db.get('SELECT * FROM templates WHERE id = ?', [id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: 'Template not found' });
    const filePath = path.join(TEMPLATES_DIR, row.filename);
    if (!fs.existsSync(filePath)) return res.status(404).json({ error: 'File not found' });
    res.sendFile(filePath);
  });
};

exports.deleteTemplate = (req, res) => {
  const id = req.params.id;
  db.get('SELECT * FROM templates WHERE id = ?', [id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ error: 'Template not found' });
    const filePath = path.join(TEMPLATES_DIR, row.filename);
    fs.unlink(filePath, (err) => {
      if (err && err.code !== 'ENOENT') return res.status(500).json({ error: err.message });
      db.run('DELETE FROM templates WHERE id = ?', [id], (err) => {
        if (err) return res.status(500).json({ error: err.message });
        res.json({ success: true });
      });
    });
  });
};