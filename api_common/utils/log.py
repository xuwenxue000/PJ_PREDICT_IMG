# -*- coding: utf-8 -*-

LOG_DEBUG_LEVEL = 10
LOG_INFO_LEVEL = 20
LOG_WARN_LEVEL = 30
LOG_ERROR_LEVEL = 40
DEFAULT_LOG_LEVEL = LOG_INFO_LEVEL

CURRENT_LOG_LEVEL = DEFAULT_LOG_LEVEL


def log(log_level,*message):
    if CURRENT_LOG_LEVEL <= log_level:
        print(message)


def debug(*message):
    log(LOG_DEBUG_LEVEL,message)


def info(*message):
    log(LOG_INFO_LEVEL, message)


def warn(*message):
    log(LOG_WARN_LEVEL, message)


def error(message):
    log(LOG_ERROR_LEVEL, message)


