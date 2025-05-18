import logging

def write_to_log(log_message):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug(log_message)