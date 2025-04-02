
def main():
    with open('encrypt.py.enc', 'rb') as file:
        enc = file.read()
    text = b'fro'
    key = [text[i] ^ enc[i] for i in range(3)]
    text = bytes([enc[i] ^ key[i % len(key)] for i in range(len(enc))])
    with open('encrypt.py', 'wb') as file:
        file.write(text)

if __name__ == "__main__":
    main()
