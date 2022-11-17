import logging
from functools import wraps

logger = None

def startLogger(config):
    """
    로거 생성
    --
    log_dir: 로그 위치
    log_level: 로그 레벨 
    """
    global logger
    if logger is None:
        logging.basicConfig(filename=config["log_dir"]+config["log_name"], level=config["log_level"])
        logger = logging.getLogger(config["log_name"])
        
def logInfo(logStr):
    """
    log decorator 
    ---
    @logInfo("메세지")
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(logStr)

            return func(*args, **kwargs)
        return wrapper
    return decorator


