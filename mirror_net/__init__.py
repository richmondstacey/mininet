"""Mininet optimized for Python3."""

import logging
import os

import coloredlogs

__version__ = '3.0.0'

logger = logging.getLogger(__name__)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG').upper()
coloredlogs.install(level='DEBUG', logger=logger)
