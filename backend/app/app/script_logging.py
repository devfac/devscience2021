import logging
import os
from datetime import date


class ScriptLogging:
    def __init__(self, filename: str):
        self.filename = filename
        try:
            path = f'/app/log'
            # Check whether the specified path exists or not
            is_exist = os.path.exists(path)
            if not is_exist:
                # Create a new directory because it does not exist
                os.makedirs(path)
                print(path)
                print("The new directory is created!")
            logging.basicConfig(
                filename=f'{path}/{self.filename}.log',
                level=logging.INFO,
                filemode="a",
            )
        except FileExistsError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)

    def script_logging(self, log_type: str, message: str) -> None:
        if log_type == "info":
            logging.info(message)
        elif log_type == "error":
            logging.error(message)
