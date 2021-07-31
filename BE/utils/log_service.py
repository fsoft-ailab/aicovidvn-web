import logging


# Get logging level
def _get_logging_level(log_level):
    if log_level == 'DEBUG':
        return logging.DEBUG
    if log_level == 'INFO':
        return logging.INFO
    if log_level == 'ERROR':
        return logging.ERROR


# Init log
def init_log(log_level):
    logging.basicConfig(filename='app.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=_get_logging_level(log_level))

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(_get_logging_level(log_level))
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


# For debug message
def debug(msg):
    logging.debug(msg)


# For info message
def info(msg):
    logging.info(msg)

# For warning message
def warning(msg):
    logging.warning(msg)


# For error message
def error(msg, exc_info=True):
    logging.error(msg, exc_info=exc_info)


# For exception message
def exception(msg):
    logging.exception(msg)
