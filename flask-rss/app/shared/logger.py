import logging
import logging.config
from config.settings import LOGGING
from flask import request as Request

class Logger():
    logging.config.dictConfig(LOGGING)
    log = logging.getLogger('gateway')
    clean_kwargs = []

    @staticmethod
    def format_msg(msg, request=Request, **kwargs):
        """
            in test cases request is empty
            because this, has multiple get, for work in test cases
        """
        headers = {} if not request else request.headers
        log_id = headers.get('idLog', 'NULL')
        req_id = headers.get('idReq', 'NULL')
        return f"ID LOG: {log_id} - ID REQ: {req_id} - {msg}"

    @classmethod
    def _log(cls, msg, *args, **kwargs):
        msg = cls.format_msg(msg, **kwargs)
        for key in cls.clean_kwargs:
            kwargs.pop(key)
        # return msg, args, kwargs
        return msg

    @classmethod
    def debug(cls, msg, *args, **kwargs):
        cls.log.debug(cls._log(msg, *args, **kwargs))

    @classmethod
    def info(cls, msg, *args, **kwargs):
        cls.log.info(cls._log(msg, *args, **kwargs))

    @classmethod
    def warning(cls, msg, *args, **kwargs):
        cls.log.warning(cls._log(msg, *args, **kwargs))

    @classmethod
    def error(cls, msg, *args, **kwargs):
        cls.log.error(cls._log(msg, *args, **kwargs))
    
    @classmethod
    def critical(cls, msg, *args, **kwargs):
        cls.log.critical(cls._log(msg, *args, **kwargs))

