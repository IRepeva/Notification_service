BASE_LOG_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - %(module)s.%(funcName)s::%(lineno)d - %(message)s"
NGINX_FORMAT = "%(asctime)s.%(msecs)03d - %(levelname)s - %(client_addr)s - %(request_id)s - '%(request_line)s' - %(status_code)s"
LOG_DEFAULT_HANDLERS = ['console', ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'base': {
            'format': BASE_LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': NGINX_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'formatter': 'base',
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        '': {
            'handlers': LOG_DEFAULT_HANDLERS,
            'level': 'INFO',
        },
        'uvicorn.error': {
            'level': 'INFO',
        },
        'uvicorn.access': {
            'handlers': ['access'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': 'INFO',
        'formatter': 'base',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}
