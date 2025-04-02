const express = require('express');
const router = express.Router();

const users = [];

router.get('/register', (req, res) => {
  res.render('register', { title: 'Регистрация' });
});

router.post('/register', (req, res) => {
  const { username, password } = req.body;
  if (!username || !password) {
    return res.send('Укажите логин и пароль!');
  }
  const existingUser = users.find(u => u.username === username);
  if (existingUser) {
    return res.send('Пользователь уже существует!');
  }
  users.push({ username, password });
  return res.redirect('/auth/login');
});

router.get('/login', (req, res) => {
  res.render('login', { title: 'Авторизация' });
});

router.post('/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username && u.password === password);
  if (!user) {
    return res.send('Неправильный логин или пароль');
  }
  req.session.user = user;
  return res.redirect('/');
});

router.get('/logout', (req, res) => {
  req.session.destroy();
  res.redirect('/');
});

module.exports = router;
