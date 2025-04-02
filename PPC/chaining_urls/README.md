# Chaining urls

|Название|Сложность|Автор|
|------|-----|-------|
|Chaining urls|Easy|[ NS ]|

# Решение

Участникам дан URL, необходимо написать парсер данных и реализовать OCR распознавание для дальнейшего продвижения.

Солвер:

```
import requests, re, sys, io, pytesseract, base64, binascii
from functools import partial
from PIL import Image


HOST = "http://127.0.0.1:13337/"
#HOST = "http://85.209.153.97:13337/"

visited_places = set()


def img2text(img: bytes) -> str:
    # 'sudo pacman -S tesseract-data-eng' to install the dataset
    text = pytesseract.image_to_string(Image.open(io.BytesIO(img)), lang="eng")
    text = text.replace("\n"," ")
    text = text.replace(". ",".")
    text = text.replace(" .",".")
    return text


def try_encoders(s: str) -> str:
    rot13_trans = bytes.maketrans(
    b'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
    b'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')
    rot13 = lambda x: x.translate(rot13_trans).encode()
    
    decoders: tuple[Callable[..., bytes],...] = (
        base64.b32decode,
        base64.b64decode,
        base64.b85decode,
        binascii.unhexlify,
        rot13
    )

    for decoder in decoders:
        try:
            dec = decoder(s)
            # print(f"dec: {dec}")
            if dec.endswith(b".html") or dec.endswith(b".png"):
                return dec.decode()
        except:
            # print(f"skip {decoder.__name__}")
            continue
    raise ValueError(f"Not encoded: {s}")


def get_next_page(page: str) -> str:
    global HOST, visited_places

    resp = requests.get(HOST + page)
    # print(resp.content)
    next_pages = None
    if resp.content[1:4] == b"PNG":
        text = img2text(resp.content)
        next_pages = re.findall("Its name is (.+)", text)[0]
    else:
        next_pages = re.findall("Its name is (.+)", resp.text)[0]
        
    # print(f"{next_pages=!r}")
    
    if " or " not in next_pages:
        next_page = next_pages.strip()
        visited_places.add(next_page)
        return next_page

    for next_page in filter(lambda el: el and el != "or", next_pages.split(" ")):
        if "." not in next_page and "png" in next_page:
            next_page = next_page.replace("png",".png")
        elif ".html" not in next_page and ".png" not in next_page:
            next_page = try_encoders(next_page)
        
        # print(f"{next_page} in visited_places: {next_page in visited_places}")
        if next_page in visited_places:
            print(f"Skipping a loop: {page} -> {next_page}")
            continue

        if requests.get(HOST + next_page).status_code == 200:
            visited_places.add(next_page)
            return next_page

    raise Exception(f"Can't find the next page in {page}:\n{resp.text[:50]}")


if __name__ == "__main__":
    i = 0
    next_page = get_next_page("1.html")
    while next_page:
        i += 1
        print(f"next page ({i}): {next_page!r}")
        next_page = get_next_page(next_page)
        # print(visited_places)
```

Первый флаг будет получен после 200 страниц, второй после 300

# Flag
RDG{You_d3finite1y_hav3_s0me_5ki11s}
RDG{3nd_of_7he_Cha1n}
Пе
