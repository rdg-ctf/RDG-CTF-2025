import socket
from helpers import NEWLINE


MSG_MAXLEN: int = 100


class MySocket:
    def __init__(self, sock: socket.socket):
        self.sock: socket.socket = sock

    def mysend(self, msg: str) -> None:
        self.sock.send(msg.encode())

    def mysendline(self, msg: str) -> None:
        self.sock.send(f"{msg}{NEWLINE}".encode())

    def myrecv(self) -> str:
        recv = self.sock.recv(MSG_MAXLEN).decode(errors="replace")
        return recv

    def myclose(self, msg: str = "", how: int = socket.SHUT_RDWR) -> None:
        try:
            if msg:
                self.mysendline(msg)
            self.sock.shutdown(how)
        except Exception:
            pass
        self.sock.close()