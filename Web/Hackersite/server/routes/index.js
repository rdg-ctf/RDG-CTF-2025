const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  res.render('home', { title: 'Главная' });
});

router.get('/about', (req, res) => {
  res.render('about', { title: 'О проекте' });
});

module.exports = router;
