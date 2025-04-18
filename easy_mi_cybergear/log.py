import logging
import colorlog

def setup_logging():
    log_format = (
        "%(asctime)s "
        "[%(log_color)s%(levelname)s%(reset)s] "
        "%(message)s"
    )
    log_colors = {
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
    }
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        log_format,
        datefmt="%m-%d %H:%M:%S",
        log_colors=log_colors,
    ))
    logging.getLogger().handlers = []
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)
# log_format = (
#     "%(asctime)s "
#     "[%(log_color)s%(levelname)s%(reset)s] "
#     "%(message)s"
# )

# log_colors = {
#     'INFO': 'green',
#     'WARNING': 'yellow',
#     'ERROR': 'red',
# }

# handler = colorlog.StreamHandler()
# handler.setFormatter(colorlog.ColoredFormatter(
#     log_format,
#     datefmt="%m-%d %H:%M:%S",
#     log_colors=log_colors,
# ))

# logging.getLogger().handlers = []
# logging.getLogger().addHandler(handler)
# logging.getLogger().setLevel(logging.INFO)