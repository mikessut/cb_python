import logging


def get_logger(fn, log_name, console=True, debug_console=False, debug_file=True):

    console_handler = logging.StreamHandler()
    if debug_console:
        console_handler.setLevel(logging.DEBUG)
    else:
        console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))

    file_handler = logging.FileHandler(fn)
    if debug_file:
        file_handler.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(message)s'))

    log = logging.getLogger(log_name)
    log.addHandler(file_handler)
    if console:
        log.addHandler(console_handler)

    log.setLevel(logging.DEBUG)
    return log
