# Pacman 

## Описание 
| Название | Сложность | TLDR | Автор |
|------|-----|-------|--------|
| Pacman | Easy | pyinstaller unpacking |[@maxhays](https://t.me/maxhays) |

---
## Решение 
При помощи Detect It Easy проевряем, на чем написан и при помощи чего упакован бинарь – Python x PyInstaller

Распаковываем pyinstaller. 

В главном исполняемом файле ничего нет. Смотрим питоновский рантайм:
Пропатчена функция floor в модуле freegames, которая ссылается на big_floor из модуля os

![image](https://github.com/user-attachments/assets/30a06d2d-4312-4f40-8abf-bdccdaebd6cf)

Видим, что в big_floor ксором распаковывается флаг.

![image](https://github.com/user-attachments/assets/ba91db68-8b1b-45ab-9b53-47d2761cd7b3)

![image](https://github.com/user-attachments/assets/53db7d25-acbb-46df-9cca-02b5a0f24be9)

# Flag
rdg{another_patched_runtime}
