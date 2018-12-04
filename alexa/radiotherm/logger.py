import logging

LOG_FILE = 'radiotherm.log'
FILE_LOG_FMT = '%(asctime)s:%(name)s:%(levelname)s:%(message)s'
CONSOLE_LOG_FMT = '%(name)s:%(levelname)s:%(message)s'

CONSOLE_LOG_LEVEL = logging.DEBUG
FILE_LOG_LEVEL = logging.DEBUG

def Logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(CONSOLE_LOG_FMT)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(CONSOLE_LOG_LEVEL)
    consoleHandler.setFormatter(formatter)

    formatter = logging.Formatter(FILE_LOG_FMT)

    fileHandler = logging.FileHandler(LOG_FILE)
    fileHandler.setLevel(FILE_LOG_LEVEL)
    fileHandler.setFormatter(formatter)

    #logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    return logger
