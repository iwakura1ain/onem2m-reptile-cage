import logging
from functools import wraps

logger = None

def startLogger(log_dir, log_level=logging.INFO):
    """
    로거 생성
    --
    log_dir: 로그 위치
    log_level: 로그 레벨 
    """
    global logger
    logging.basicConfig(filename="test.log", level=logging.INFO)
    logger = logging.getLogger("test")   

    
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


