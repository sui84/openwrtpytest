#!/mnt/sda1/opkg/usr/bin/python
import functools
import logging

    
def exception(logger):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
 
    @param logger: The logging object
    """
 
    def decorator(func):
 
        def wrapper(*args, **kwargs):
            try:
                msg = "funcname=%s,args=%s,kwargs=%s" % (func.__name__ ,args , kwargs)
                logger.info(msg)
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "exception : funcname=%s,args=%s,kwargs=%s" % (func.__name__ ,args , kwargs)
                logger.exception(err)
 
            # re-raise the exception
            raise
        return wrapper
    return decorator
    
    
def create_logger(logpath='/mnt/sda1/temp/log'):
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("testlogger")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler(logpath)
 
    fmt = '[%(asctime)s - %(name)s - %(levelname)s %(process)d %(processName)s %(thread)d %(threadName)s] %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger

logger = create_logger('/mnt/sda1/temp/log')
@exception(logger)
def zero_divide(i,j):
    i/j

if __name__ == '__main__':
    #zero_divide(1,0)
    zero_divide(1,1)
