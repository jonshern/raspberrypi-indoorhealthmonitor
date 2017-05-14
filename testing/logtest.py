import time
import logging
import json
import sys

def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # create a file handler
    handler = logging.FileHandler('sensorlogger.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    logger.info('Start logging sensor readings')


if __name__ == '__main__':
    main()

