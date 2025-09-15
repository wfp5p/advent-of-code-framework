import os
import sys


def LoguruConfig():
    lg_handler = {
        'sink': sys.stderr,
        'level': 'INFO',
        'format': '<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>',
    }

    if level := os.getenv('LOGURU_LEVEL'):
        lg_handler['level'] = level

    if lg_format := os.getenv('LOGURU_FORMAT'):
        lg_handler['format'] = lg_format

    return lg_handler
