#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from loguru import logger
from worker import Facade
from config import log_config


if __name__ == "__main__":
    logger.configure(**log_config)
    facade = Facade()
    facade.start()
