import os, sys, socket, psutil, traceback
from ClientThread import ClientThread
from MyLogger import MyLogger
from helpers import NEWLINE


LPORT: int = int(sys.argv[1]) if len(sys.argv) > 1 else 51337
LHOST: str =  "0.0.0.0"
try:
    CON_LIMIT: int = int(os.getenv("MAXCON"))
except:
    CON_LIMIT: int = 3


def is_connections_limit_exceeded(ip: str, limit: int) -> bool:
    """
    Simple ipv4 connections limitation.
    Return True if the current host already has more connections than the limit.
    Return False otherwise.
    """
    established: int = 0
    for con in psutil.net_connections(kind="tcp"):
        if con.status == "ESTABLISHED" \
        and con.family == socket.AF_INET \
        and hasattr(con.raddr, "ip") \
        and con.raddr.ip == ip:
            #print(con)
            established += 1
    return True if established > limit else False


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server_socket.bind((LHOST, LPORT))
    server_socket.listen(1000)
    logger: MyLogger = MyLogger("server")
    logger.info(f"Listening on {(LHOST, LPORT)}")
    while True:
        try:
            logger.info("Accepting...")
            (client_socket, address) = server_socket.accept()
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt")
            break
        if is_connections_limit_exceeded(ip = address[0], limit = CON_LIMIT):
            logger.info(f"Connection refused from {address}. Too many connections. ")
            client_socket.sendall(f"Too many connections from your IP {NEWLINE}".encode())
            client_socket.shutdown(socket.SHUT_RDWR)
            client_socket.close()
            continue
        logger.info(f"Connection received from {address}")
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        client_socket.settimeout(15)
        try:
            thread = ClientThread(socket = client_socket)
            thread.start()
        except Exception:
            logger.error(f"Error starting a game with {address}: {NEWLINE}{traceback.format_exc()}")
    logger.info("Shutting down the server")
    server_socket.close()

