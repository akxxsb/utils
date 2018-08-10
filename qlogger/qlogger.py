# -*- coding:utf-8 -*-
#!/usr/bin/env python
import logging
import logging.handlers

def get_logger(logger_name, filename=None, level=logging.INFO, when='d', 
        interval=1, backupCount=7, encoding=None, utc=False, 
        fmt='%(asctime)s %(levelname)s tid:%(thread)d %(filename)s:%(funcName)s:%(lineno)d %(message)s'):
    logger = logging.Logger(name=logger_name, level=level)

    formatter = logging.Formatter(fmt=fmt)

    stderr_handler = logging.StreamHandler()
    stderr_handler.setFormatter(formatter)

    if filename is not None:

        info_handler = logging.handlers.TimedRotatingFileHandler(filename=filename, when=when, interval=interval, 
                backupCount=backupCount, encoding=encoding, utc=utc)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        wf_handler = logging.handlers.TimedRotatingFileHandler(filename=filename+'.wf', when=when, interval=interval, 
                backupCount=backupCount, encoding=encoding, utc=utc)
        wf_handler.setLevel(logging.WARNING)
        wf_handler.setFormatter(formatter)

        logger.addHandler(info_handler)
        logger.addHandler(wf_handler)

    logger.addHandler(stderr_handler)

    return logger

_default_logger = None

def get_default_logger():
    global _default_logger
    if _default_logger:
        return _default_logger
    _default_logger = get_logger(logger_name='default', filename='run.log')
    return _default_logger

def test():
    logger = get_default_logger()
    logger.debug('test debug')
    logger.info('test info')
    logger.warn('test warn')
    logger.warning('test warning')
    try:
        dict().test()
    except Exception as ex:
        logger.exception(ex)
        logger.error(ex)
    logger.critical('test critical')
    logger.fatal('test fatal')

if __name__ == '__main__':
    test()
