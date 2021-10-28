import logging


LOG_FORMAT = ('%(levelname) -10s %(asctime) '
              '-30s: %(message)s')
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)