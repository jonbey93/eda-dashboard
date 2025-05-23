import logging

def setup_logging():
    logging.basicConfig(
    level=logging.WARNING,
    filename='debugging.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def write_to_log(log_message):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.debug(log_message)