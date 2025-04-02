import random, pathlib, shutil, string, sys, base64, binascii, html2image
from pprint import pprint
from typing import Any, Callable
from SingleLinkedList import SingleLinkedList
from helpers import *


randint_page = lambda: random.randint(10**50, 10**51)
page_letters = string.digits + string.ascii_letters


def generate_keys(
        sll: SingleLinkedList, 
        incremental_range: range,
        randint_range: range,
        encodings_range: range,
        image_range: range
    ) -> None:
    global page_letters, randint_page

    for i in incremental_range:
        sll.add(str(i))
    
    r: str = ""
    for _ in randint_range:
        r = str(randint_page())
        while r in sll:
            r = str(randint_page())
        sll.add(r)

    name: str = ""
    for _ in encodings_range:
        name = "".join(random.choice(page_letters) for _ in range(10))
        while len(name) > 0 and name in sll:
            name = "".join(random.choice(page_letters) for _ in range(10))
        sll.add(name)

    for _ in image_range:
        r = str(randint_page())
        while r in sll:
            r = str(randint_page())
        sll.add(r)


def generate_pages(
        pages: dict[str,str], 
        names: SingleLinkedList,
        incremental_range: range,
        randint_range: range,
        encodings_range: range,
        image_range: range
    ) -> None:
    global page_letters, randint_page

    page_name: str = ""
    fake_names: int = 0
    fake_names_max: int = 9

    rot13_trans = bytes.maketrans(
    b'ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz',
    b'NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm')
    rot13 = lambda x: x.translate(rot13_trans)
    
    encoders: tuple[Callable[..., bytes],...] = (
        base64.b32encode,
        base64.b64encode,
        base64.b85encode,
        binascii.hexlify,
        rot13
    )
    places_to_return = []
    page_is_generated = "This page is generated automatically and the next page is generated too. Its name is "

    for i, (k, v) in enumerate(names.traverse()):
        page_name: str = f"{k}.html"
        match i+int(names.start):
            case i if i in incremental_range:
                next_page_name: str = f"{v}.html"
            case i if i in randint_range:
                next_names = []
                ext = ".html"
                if fake_names < fake_names_max and random.random() > .97:
                    fake_names += 1
                for _ in range(fake_names):
                    if len(places_to_return) > fake_names and random.random() > 0.96: # make a loop
                        place_to_return = None
                        while place_to_return is None or place_to_return in next_names:
                            place_to_return = random.choice(places_to_return)
                        next_names.append(place_to_return)
                        print(f"Made a loop: {k} -> {place_to_return} (at {int(names.start) + len(incremental_range) + places_to_return.index(place_to_return)})")
                    else:
                        next_names.append(randint_page())
                next_names.append(v)
                random.shuffle(next_names)
                next_page_name = " or ".join(f"{name}{ext}" for name in next_names)
                places_to_return.append(k)
            case i if i in encodings_range:
                next_names = []
                ext = ".png" if i + 1 in image_range else ".html"
                if fake_names < fake_names_max and random.random() > .97:
                    fake_names += 1
                for _ in range(fake_names):
                    if len(places_to_return) > fake_names and random.random() > 0.96: # make a loop
                        place_to_return = None
                        while place_to_return is None or place_to_return in next_names:
                            place_to_return = random.choice(places_to_return)
                        next_names.append(place_to_return)
                        print(f"Made a loop: {k} -> {place_to_return} (at {int(names.start) + len(incremental_range) + places_to_return.index(place_to_return)})")
                    else:
                        name = "".join(random.choice(page_letters) for _ in range(10))
                        while name in names:
                            name = "".join(random.choice(page_letters) for _ in range(10))
                        next_names.append(name)
                next_names.append(v)
                random.shuffle(next_names)
                encoder = random.choice(encoders)
                next_page_name = " or ".join(encoder(f"{name}{ext}".encode()).decode() for name in next_names)
                places_to_return.append(k)
            case i if i in image_range:
                page_name = f"{k}.png"
                next_names = []
                if fake_names < fake_names_max and random.random() > .97:
                    fake_names += 1
                for _ in range(fake_names):
                    next_names.append(f"{randint_page()}.png")
                if v != names.start:
                    next_names.append(f"{v}.png")
                random.shuffle(next_names)
                next_page_name = " or ".join(name for name in next_names)
            case _:
                raise NotImplementedError
        next_page_name = page_is_generated + next_page_name
        if i == int(names.start):
            header = "<h1>Welcome to My Website</h1>"
        elif i in encodings_range and i+1 not in encodings_range:            
            header = f"<h1>Congratulations!</h1>\nCheck out the flag: {FLAG1}"
            print(f"Generated FLAG page: {k} : {FLAG1}")
        elif i in image_range and i+1 not in image_range:
            header = f"<h1>Congratulations!</h1>\nCheck out the flag2: {FLAG2}"
            next_page_name = ""
            print(f"Generated FLAG page: {k} : {FLAG2}")
        else:
            header = ""
        pages[page_name] = PAGE_BODY.format(header = header, next_page = next_page_name)
        print(f"{page_name=},{next_page_name=}")
        if i%10 == 0:
            print(f"Generated {i} pages")


def write_pages(pages: dict[str,str], root_dir: pathlib.Path, image_range: range) -> None:
    hti = html2image.Html2Image(
        output_path=root_dir,
        browser_executable="/usr/bin/chromium",
        custom_flags="--headless")
    html_str = []
    save_as = []
    for i, (k, v) in enumerate(pages.items()):
        if i+1 in image_range:
            html_str.append(v)
            save_as.append(k)
        else:
            with open(root_dir /  k, "w") as fout:
                fout.write(v)
        if i%10 == 0:
            print(f"Written {i} pages")

    assert len(html_str) == len(save_as)
    hti.screenshot(
        html_str=html_str,
        save_as=save_as
    )


if __name__ == "__main__":
    names = SingleLinkedList()
    incremental_range = range(1, 11)
    randint_range = range(11, 101)
    encodings_range = range(101, 201)
    image_range = range(201, 301)

    generate_keys(
        names,
        incremental_range,
        randint_range,
        encodings_range,
        image_range
    )
    print(names.keys())

    pages: dict[str,str] = dict()
    generate_pages(
        pages, 
        names,
        incremental_range,
        randint_range,
        encodings_range,
        image_range
    )
    assert len(names) == len(pages)
    # pprint(pages)

    if "-w" in sys.argv:
        root_dir = pathlib.Path("www")
        if (root_dir).exists():
            shutil.rmtree(root_dir)
        root_dir.mkdir()

        write_pages(pages, root_dir, image_range)

