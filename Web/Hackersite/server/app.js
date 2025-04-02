const express = require('express');
const path = require('path');
const session = require('express-session');
const expressLayouts = require('express-ejs-layouts');

const indexRoutes = require('./routes/index');
const authRoutes = require('./routes/auth');
const mdRoutes = require('./routes/markdown');

const app = express();

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(expressLayouts);
app.set('layout', 'layout');

app.use(express.static(path.join(__dirname, 'public')));
app.use(express.urlencoded({ extended: false }));

app.use(session({
  secret: 'tretrwtyrhtrhrtwehrthetrhtrhdtdhthththdthtdhdhthdththht4353w545445twest45w3',
  resave: false,
  saveUninitialized: false
}));

app.use((req, res, next) => {
  res.locals.session = req.session;
  next();
});

app.use('/', indexRoutes);
app.use('/auth', authRoutes);
app.use('/markdown', mdRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
