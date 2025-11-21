import datetime
from pathlib import Path

error_file = Path("log.log")

if not error_file.exists():
    error_file.touch()


def log_error(message: str):
    with open(error_file, "a") as log_file:
        log_file.write("*" * 20 + "\n")
        log_file.write(str(datetime.datetime.now()) + "\n")
        log_file.write(message + "\n")
        log_file.write("*" * 20 + "\n")
    print(message)


def log_info(message: str):
    with open(error_file, "a") as log_file:
        log_file.write("-" * 20 + "\n")
        log_file.write(str(datetime.datetime.now()) + "\n")
        log_file.write(message + "\n")
        log_file.write("-" * 20 + "\n")
    print(message)
