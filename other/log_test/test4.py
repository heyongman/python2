# coding=utf-8
import logging.config
import time
import test2

config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },
        # 其他的 formatter
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logging.log',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'rotaFile': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'rota_logging.log',
            'level': 'DEBUG',
            'formatter': 'simple',
            'when': 'd',
            'interval': 1,
            'backupCount': 5
        },
        # 其他的 handler
    },
    'loggers': {
        'StreamLogger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'ConsoleFileLogger': {
            # 既有 console Handler，还有 file Handler
            'handlers': ['console', 'file', 'rotaFile'],
            'level': 'DEBUG',
        },
        # 其他的 Logger
    }
}

logging.config.dictConfig(config)
StreamLogger = logging.getLogger("StreamLogger")
ConsoleFileLogger = logging.getLogger("ConsoleFileLogger")

if __name__ == '__main__':
    while True:
        ConsoleFileLogger.debug('debug')
        ConsoleFileLogger.info('info')
        ConsoleFileLogger.warn('warn')
        ConsoleFileLogger.error('error')

        test2.main()

        time.sleep(5)
