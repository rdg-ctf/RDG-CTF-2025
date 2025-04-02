# strange_file 

## Описание 
| Название | Сложность | TLDR | Автор |
|------|-----|-------|--------|
| strange_file | Medium | dynamic import research with antidebug patching |[@maxhays](https://t.me/maxhays) |

---
## Решение 
Ключевым моментом в понимании исходного кола является понимание того, что импорты динамически подгружаются во время исполнения файла.

Отловить сразу в динамике не получится из-за постоянной проверки на дебаг. Их количество:

![1743571062782](https://github.com/user-attachments/assets/b044fede-82d9-435d-bc72-e3d626e5588c)

В коде и ассемблере они выглядят так:

![1743571147428](https://github.com/user-attachments/assets/9bcd7acd-560b-4d83-902b-a7531c4d86fe)

![1743571179416](https://github.com/user-attachments/assets/2fa49c03-ff25-4d8c-8266-08f4333ce8d7)


Тут существует несколько путей. 

Первый, постоянно в отладчике менять значение функции, которая проверяет на отладку, чтобы проверка проходила дальше. 

![1743572866099](https://github.com/user-attachments/assets/f431926a-05e3-46a0-958c-508111abbf5f)
 
Второй, пропатчить все проверки на дебаг. 

![1743571553362](https://github.com/user-attachments/assets/fbddc056-39e9-4a36-8dab-c16b328b6664)

![1743571507143](https://github.com/user-attachments/assets/25def4ee-0f54-4872-8dda-c47304c930f5)

И третий, разобраться с алгоритмом в статикею.

После множества проверок на дебаг, в регистре eax можно увидеть флаг в открытом виде.

На данном этапе: 

![1743573802729](https://github.com/user-attachments/assets/dbac46c5-45c1-42ff-bc4e-06c7e14be3dc)

Смотрим что лежит в регистре `EAX`:

![1743573889098](https://github.com/user-attachments/assets/98f117e4-09ad-4b0d-9b6b-a1c1281f1516)

И находим там флаг:

![1743573478759](https://github.com/user-attachments/assets/5a8da204-3100-4649-acc0-1a20e6c7ab7d)

# Flag
rdg{str4ng3_1mp0rts_l00ks_l1k3_m4lw4r3}
