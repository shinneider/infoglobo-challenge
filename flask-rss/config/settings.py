from decouple import config

RSS_URL = config('RSS_URL')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=True)

# Application definition

ROOT_URLCONF = 'config.urls'

# Python Logging Dict Config
# https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'gateway': {
            'format': '[%(asctime)s] [%(levelname)s] RSS - %(message)s',
        }
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './logs/requests.log',
            'formatter': 'gateway',
        },
    },
    'loggers': {
        'gateway': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
