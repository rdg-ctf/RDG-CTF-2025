import threading
from typing import Callable
from traceback import format_exc
from MyLogger import MyLogger
from MySocket import MySocket
from helpers import NEWLINE, INTRO, CONGRATULATIONS, FLAG, TROLLFACE
from mycalc import get_answer, smart_convert, mysplit
from levels import (
    level_1,
    level_2,
    level_3,
    level_4,
    level_5,
    level_6,
    level_7,
    level_8,
    level_9,
    level_10
)


ALL_LEVELS: tuple[Callable, ...] = (
    level_1,
    level_2,
    level_3,
    level_4,
    level_5,
    level_6,
    level_7,
    level_8,
    level_9,
    level_10
)

TEST_LEVELS: tuple[Callable, ...] = (
    level_1,
    level_4,
    level_6,
    level_10
)


class ClientThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        socket = kwargs.pop("socket")
        super().__init__(*args, **kwargs)
        self.steps_completed = 0
        self.mysock: MySocket = MySocket(socket)
        address, port = socket.getpeername()
        self.peername: str = f"{address}_{port}"
        self.logger: MyLogger

    def run(self) -> None:
        """
        Initialise logger here and run the thread body
        """
        with MyLogger(self.peername) as logger:
            self.logger = logger
            try:
                self._menu()
            except BrokenPipeError:
                self.logger.info("Disconnected from client. ")
            except TimeoutError:
                self.logger.info("Timeouted or closed from client. ")
                self.mysock.mysendline(NEWLINE + "Too late... Bring a pocket calculator next time.")
            except Exception:
                self.logger.error(f"Got exception: {NEWLINE}{format_exc()}")

    def _menu(self) -> None:
        """
        Work with the instance of MySocket here.
        """
        self.mysock.mysendline(INTRO)

        while True:
            self.mysock.mysend(NEWLINE + """Actions available:
\t0 - Exit.
\t1 - Start test (no rewards).
\t2 - Start game.
\t3 - Get the flag.
Choice: """)
            recv = self.mysock.myrecv().strip()
            match recv:
                case "0":
                    pass
                case "1":
                    self._test()
                    continue
                case "2":
                    self._game()
                case "3":
                    self.mysock.mysendline(TROLLFACE)
                case _:
                    continue
            break

        self.mysock.myclose("Bye!")
        return

    def _test(self) -> None:
        # A simpler game version with only one round in a few levels, without the flag
        levels_completed: int = 0
        for level in TEST_LEVELS:
            term: str = level(1)
            answer = get_answer(mysplit(term))
            self.mysock.mysend(f"{term} == ")
            client_answer = self.mysock.myrecv().strip()
            if smart_convert(client_answer) != answer:
                self.logger.debug(f"Test mismatch: term: {term}")
                self.logger.debug(f"Test mismatch: answer: {answer}, client_answer: {client_answer}")
                self.mysock.mysendline("Incorrect :(")
                return
            levels_completed += 1
        if levels_completed == len(TEST_LEVELS):
            self.logger.info("Passed the test")
            self.mysock.mysendline("Passed.")
        return

    def _game(self) -> None:
        levels_completed: int = 0
        rounds_completed: int = 0

        for level in ALL_LEVELS:
            rounds_completed = 0
            for _round in range(1,11):
                term: str = level(_round)
                answer = get_answer(mysplit(term))
                self.mysock.mysend(f"{term} == ")
                client_answer = self.mysock.myrecv().strip()
                if smart_convert(client_answer) != answer:
                    self.logger.debug(f"Mismatch: term: {term}")
                    self.logger.info(f"Mismatch: answer: {answer}, client_answer: {client_answer}")
                    self.mysock.mysendline("Incorrect :(")
                    return
                else:
                    self.logger.debug(f"answer: {answer}, client_answer: {client_answer}")
                rounds_completed += 1
            if rounds_completed != 10:
                break
            levels_completed += 1
            self.logger.info(f"Completed level {levels_completed}")
        
        if levels_completed == len(ALL_LEVELS) and rounds_completed == 10:
            self.mysock.mysendline(CONGRATULATIONS)
            self.mysock.mysendline(FLAG)
            self.logger.info("The flag has been sent")

        return

