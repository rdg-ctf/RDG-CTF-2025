from typing import Self
from pathlib import Path
import logging, sys, os


class MyLogger(logging.Logger):
    dirname: str = "logs"

    def __init__(self, name: str, level: int | str = logging.INFO) -> None:
        super().__init__(name, level)
        if self.try_create_dir():
            self._setup_logger()

    def _setup_logger(self) -> None:
        self.setLevel(logging.INFO)
        self.addHandler(logging.StreamHandler(sys.stdout))
        self.addHandler(logging.FileHandler(str(Path.cwd() / Path(__class__.dirname) / (self.name + ".txt"))))
        for handler in self.handlers:
            handler.setFormatter(logging.Formatter(f"%(asctime)s [%(levelname)s] ({self.name}) %(message)s", "%Y-%m-%d %H:%M:%S"))

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for handler in self.handlers:
            self.removeHandler(hdlr=handler)
        for filter in self.filters:
            self.removeFilter(filter=filter)

    @staticmethod
    def try_create_dir() -> bool:
        if not (Path.cwd() / __class__.dirname).exists():
            try:
                os.mkdir(__class__.dirname, mode=0o744)
                print(f"Created dir {__class__.dirname}")
            except Exception:
                print("Can't create logs folder")
                return False
        return True
        