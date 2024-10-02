#- log.py -#

class Log:
    COLOR_RESET = "\033[0m"
    COLOR_INFO = "\033[94m"
    COLOR_WARN = "\033[93m"
    COLOR_ERROR = "\033[91m"
    
    def __init__(self) -> None:
        pass
    
    def info(self, statement="") -> None:
        print(f"{self.COLOR_INFO}[INFO]: {statement}{self.COLOR_RESET}")
        
    def error(self, statement="") -> None:
        print(f"{self.COLOR_ERROR}[ERROR]: {statement}{self.COLOR_RESET}")
        
    def warn(self, statement="") -> None:
        print(f"{self.COLOR_WARN}[WARN]: {statement}{self.COLOR_RESET}")