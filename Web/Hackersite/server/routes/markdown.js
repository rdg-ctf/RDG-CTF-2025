const express = require('express');
const router = express.Router();
const { exec } = require('child_process');
const requireAuth = require('../helpers/authMiddleware');

router.get('/', requireAuth, (req, res) => {
  res.render('markdown', { title: 'Markdown Playground', output: null });
});

router.post('/', requireAuth, (req, res) => {
  const markdownContent = req.body.markdownContent || '';

  const sanitizedInput = markdownContent
    .replace(/`/g, '')
    .replace(/;/g, '')
    .replace(/\(/g, '')
    .replace(/\)/g, '')
    .replace(/\|/g, '')
    .replace(/&/g, '')
    .replace(/cat/gi, '');

  exec(`echo "${sanitizedInput}" | pandoc -f markdown -t html`, (error, stdout, stderr) => {
    if (error) {
      return res.render('markdown', { title: 'Markdown Playground', output: error.toString() });
    }
    return res.render('markdown', { title: 'Markdown Playground', output: stdout });
  });
});

module.exports = router;
