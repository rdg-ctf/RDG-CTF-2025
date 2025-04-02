from socket import *
from mycalc import get_answer, mysplit


#HOST = "85.209.153.97"
HOST = "127.0.0.1"
PORT = 51337


if __name__ == "__main__":
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))
    text = s.recv(20_000)
    answer = b"2"
    s.send(answer)
    while True:
        text = s.recv(20_000).decode(errors="replace")
        if text == "":
            break
        if text.endswith(" == "):
            answer = get_answer(mysplit(text.replace("==","")))
            print(text, answer)
            s.send(str(answer).encode())
        else:
            print(text)
    s.close()
    print("END")

