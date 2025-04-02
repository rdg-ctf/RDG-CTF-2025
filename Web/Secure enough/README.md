# Secure Enough

## Описание:


| Название | Сложность | Автор |
|------|-----|-------|
| Secure Enough | Medium |[@collapsz](https://t.me/collapsz) |

## TLDR:

**2FA bypass** via **session puzzling**

---
## Решение:

Поскольку нам предоставлен исходный код приложения, приступим к его изучению. 

Приложение представляет из себя серверную часть на Python и микросервис для работы с 2FA на GO. 

Код микросервиса при решении данного задания не представляет большого интереса. Он просто генерирует пару secret + otp и выполняет функцию их верификации при прохождении 2FA. Наша же задача найти способ попасть в аккаунт админа без использования 2FA, посмотрим на код Flask-приложения.   

При запуске инициализируется база данных, откуда мы можем получить пользователя – `sasha_gendir:sasha_gendir`

```
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY, 
                username TEXT UNIQUE, 
                password TEXT,
                email TEXT,
                otp_secret TEXT,
                is_admin INTEGER DEFAULT 0,
                two_fa_enabled INTEGER DEFAULT 0)''')

    users = [
        ('admin', 'REDACTED', 'admin@ares.ru', 'REDACTED', 1, 1),
        ('sasha_gendir', 'sasha_gendir', 'sasha_gendir@ares.ru', 'REDACTED', 0, 0)
    ]
    
    for user in users:
        try:
            c.execute("INSERT INTO users (username, password, email, otp_secret, is_admin, two_fa_enabled) VALUES (?, ?, ?, ?, ?, ?)", user)
        except sqlite3.IntegrityError:
            pass
    
    conn.commit()
    conn.close()
```

В этом же коде видим, что в базе данных содержится столбец, отвечающий за наличие 2FA у пользователя. У админа она включена, у саши-гендира – нет

```
    users = [
        ('admin', 'REDACTED', 'admin@ares.ru', 'REDACTED', 1, 1),
        ('sasha_gendir', 'sasha_gendir', 'sasha_gendir@ares.ru', 'REDACTED', 0, 0)
    ]
```

На `/login` видим, что если пользователь вводит валидные учетные данные, ему назначается кука `session['user_id']`, затем, если у него включена 2FA, он проваливается на `/verify_2fa` и ему назначается кука `session['otp_requirued'] = True`. В случае успешной авторизации пользователю назначается кука `session['authentificated']=True` и он проваливается на `/my_profile`. 

```
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', 
                           (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            if user['two_fa_enabled']:
                session['otp_required'] = True
                return redirect(url_for('verify_2fa'))
            else:
                session['authenticated'] = True
                return redirect(url_for('my_profile'))
        return render_template('login.html', error_message="Invalid credentials")
    return render_template('login.html', error_message="")
```

Эндпоинт `/forgot` предоставляет функционал смены пароля и просит от пользователя только `username`. В случае если пользователь существует, назначается кука `session['user_id']=user['id']` – тот айдишник, что принадлежит пользователю с "забытым" паролем, выполняется запрос на микросервис для генерации секрета и OTP, секрет вносится в БД, OTP отправляется пользователю, а пользователя перенаправляет на страницу `/link_sent`

```
@app.route('/forgot', methods=['GET','POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        conn = get_db()
        user = conn.execute ("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['otp_required'] = True
            response = requests.get(f"{TWO_FA_SERVICE}/generate-secret")
            if response.status_code == 200:
                secret_data = response.json()
                otp_secret = secret_data['secret']

            conn = get_db()
            conn.execute("UPDATE users SET otp_secret = ? WHERE username = ?", (otp_secret, username))
            conn.commit()
            conn.close()

            return redirect(url_for('link_sent'))

        return render_template('forget_pass.html', error_message="User not found", success_message="")
    return render_template('forget_pass.html')
```

Сразу после этого пользователю сообщают о том, что ему выслана ссылка на смену пароля, а сессия очищается: 

```
@app.route('/link_sent')
def link_sent():
    success_message = 'Password reset link has been sent'
    session.clear()
    return render_template('forget_pass.html', success_message=success_message)
```


На этом этапе мы уже можем увидеть, что такой менеджмент сессий не является безопасным, поскольку сессия пользователя, который проходит авторизацию без OTP выглядит как: 

| Before no-OTP Auth               | After no-OTP Auth          |
|-------------------------------|-------------------------------|
| session['user_id'] = `<id>`     | session['user_id'] = `<id>`     |
| session['otp_required'] = False| session['otp_required'] = False|
| session['authentificated'] = False | session['authentificated'] = True |

В то время как пользователя, проходящего процедуру восстановления пароля: 

| Before password reset               | After password reset    |
|-------------------------------|-------------------------------|
|   none                        | session['user_id'] = `<id>`   |
|  none                         | session['otp_required'] = True|

При этом никакого контроля сессий не происходит, а `user_id` назначается без проверки, действительно ли пользователь, проходящий процедуру восстановления пароля, является таковым. 

Таким образом, мы можем собрать нужный нам набор сессионных переменных самостоятельно: 

| Before Attack               | After Attack                |
|-------------------------------|-------------------------------|
| session['user_id'] = 2    | session['user_id'] = 1     |
| session['otp_required'] = False| session['otp_required'] = False|
| session['authentificated'] = False | session['authentificated'] = True |

Для этого отправляемся на страницу `/login` и вводим креды пользователя без 2FA, попадаем на `/my_profile`:

<img width="1394" alt="изображение" src="https://github.com/user-attachments/assets/aaf1717f-8cb8-4730-836a-22c02d0d4de1" />

После этого открываем новую вкладку браузера, отправляемся на `/forgot` и вводим `admin`, отправляем запрос:

<img width="1130" alt="изображение" src="https://github.com/user-attachments/assets/a97af0d5-b5c9-439c-86f7-c5cae7848eb7" />

Затем, получив запрос с перенаправлением на `/link_sent`, меняем путь с `link_sent` на `/my_profile`, не давая сессии очиститься:

<img width="1130" alt="изображение" src="https://github.com/user-attachments/assets/08d85f17-2bf1-4598-974b-ce0cf9486a02" />

<img width="1119" alt="изображение" src="https://github.com/user-attachments/assets/a7c65cdd-3016-4b76-ab63-ee02006693de" />

Сразу после этого оказываемся в профиле админа:

<img width="1480" alt="изображение" src="https://github.com/user-attachments/assets/e426e237-4218-4615-9eaf-7e5a5c884a5e" />

## Flag:
rdg{2fa_byp455_5ucc355Fu11_ou34pdwseklm}
