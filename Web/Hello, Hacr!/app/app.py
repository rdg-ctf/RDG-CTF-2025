from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
import markdown
import os
from flask_talisman import Talisman


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jk;ndfgszipjnadfgsio[jeafsop[]jdfgznop[jk]]'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config.update(
    SESSION_COOKIE_HTTPONLY=True
)

csp = {
    'default-src': "'self'",
    'script-src': ["'self'", "'nonce-matrixrain'"],
    'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://fonts.gstatic.com"],
    'img-src': ["'self'"],
    'font-src': ["'self'", "https://fonts.gstatic.com"],
    'frame-src': ["'self'"],
    'object-src': "'none'",
    'base-uri': ["'self'"]
}

Talisman(
    app,
    content_security_policy=csp,
    force_https=False,
    strict_transport_security=False,
)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_moderated = db.Column(db.Boolean, default=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='articles')

if os.path.exists('instance/site.db'):
    os.remove('instance/site.db')

with app.app_context():
    db.create_all()
    new_user = User(username='admin', password='ipuhdfgsipuhbvfipujndfgsiuph', is_admin=1)
    db.session.add(new_user)
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            flash("This username already exists!", "danger")
            message = "This username already exists!"
            return render_template('register.html', message=message, form=form)
        else:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful!", 'success')
            return redirect(url_for('login'))

    return render_template('register.html', form=form)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect username or password", "danger")
    return render_template('login.html', form=form)

class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('new_password', validators=[DataRequired()])
    submit = SubmitField('submit')

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        new_password = form.new_password.data
        if new_password == current_user.password:
            message = "New password cannot match the previous one!"
            return render_template('change_password.html',message=message, form=form)
        current_user.password = new_password
        db.session.commit()
        message = "Password has been changed!"
        return render_template('change_password.html', message = message, form=form)
    return render_template('change_password.html', message='', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    articles = current_user.articles
    return render_template('dashboard.html', articles=articles)

class ArticleFormWrite(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/write_article', methods=['GET', 'POST'])
@login_required
def write_article():
    form = ArticleFormWrite()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_article = Article(title=title, content=content, author_id=current_user.id)
        db.session.add(new_article)
        db.session.commit()
        flash('Статья отправлена на модерацию!', 'success')
        return redirect(url_for('index'))
    return render_template('write_article.html', form=form)

@app.route('/article/<int:article_id>', methods=['GET'])
@login_required
def view_user_article(article_id):
    article = Article.query.get_or_404(article_id)

    if article.author_id != current_user.id:
        flash('У вас нет доступа к этой статье', 'danger')
        return redirect(url_for('dashboard'))

    article_content_html = markdown.markdown(article.content)
    return render_template('view_user_article.html', article=article, article_content_html=article_content_html)

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))
    articles = Article.query.filter_by(is_moderated=False).all()
    return render_template('admin.html', articles=articles)

@app.route('/admin/article/<int:article_id>', methods=['GET'])
@login_required
def view_article(article_id):
    if not current_user.is_admin:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    article = Article.query.get_or_404(article_id)
    article_content_html = markdown.markdown(article.content) 
    return render_template('view_article.html',article=article, article_content_html=article_content_html)

@app.route('/admin/decline_article/<int:article_id>', methods=['POST'])
@login_required
def decline_article(article_id):
    if not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))

    article = Article.query.get_or_404(article_id)
    article.is_moderated = True
    db.session.commit()
    flash('Article is declined!', 'fail')
    return redirect(url_for('admin'))

@app.route('/admin/approve_article/<int:article_id>', methods=['POST'])
@login_required
def approve_article(article_id):
    if not current_user.is_admin:
        flash('Access denied!', 'danger')
        return redirect(url_for('index'))

    article = Article.query.get_or_404(article_id)
    article.is_moderated = True
    db.session.commit()
    flash('Article is approved!', 'success')
    return redirect(url_for('admin'))

csrf.exempt(decline_article)
csrf.exempt(approve_article)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)

