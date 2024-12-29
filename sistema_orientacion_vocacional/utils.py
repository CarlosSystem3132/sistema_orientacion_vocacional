import logging

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# Configurar loggers
access_logger = setup_logger('access_log', 'logs/access.log')
error_logger = setup_logger('error_log', 'logs/error.log', level=logging.ERROR)