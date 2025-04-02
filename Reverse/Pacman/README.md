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



Видим, что в big_floor ксором распаковывается флаг.

# Flag
rdg{another_patched_runtime}