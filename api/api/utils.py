import logging


def configure_loggers():
    default_format = '%(asctime)s %(levelname)s\t%(name)s:\t%(message)s'
    default_date_format = '%H:%M:%S'
    default_formatter = logging.Formatter(default_format, default_date_format)

    logging.basicConfig(
        level=logging.INFO,
        format=default_format,
        datefmt=default_date_format
    )

    mainLoggerHandler = logging.StreamHandler()
    mainLoggerHandler.setFormatter(default_formatter)
    mainLogger = logging.getLogger('main')
    mainLogger.setLevel(logging.DEBUG)
    mainLogger.addHandler(mainLoggerHandler)
