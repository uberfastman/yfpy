__author__ = "Wren J. R. (uberfastman)"
__email__ = "uberfastman@uberfastman.dev"


from logging import getLogger, Logger, Formatter, StreamHandler


def get_logger(name, level=None) -> Logger:

    logger = getLogger(name)
    if len(logger.handlers) > 0:
        logger.handlers = []
    if level:
        logger.setLevel(level)

    sh = StreamHandler()
    if level:
        sh.setLevel(level)

    formatter = Formatter(
        fmt="%(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s - %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    sh.setFormatter(formatter)

    logger.addHandler(sh)

    return logger
