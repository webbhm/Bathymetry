'''Wrapper for the Python Logger to add standard MVP customization
'''
import logging
from logging.handlers import TimedRotatingFileHandler

class Logger(object):

    DETAIL = 5
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    ERROR = logging.ERROR
    lvl = {0: DETAIL, 1: DEBUG, 2: INFO, 3: ERROR}

    def __init__(self, name, lvl=INFO, file=None):
        """Create and return a logger

        Builds a Python logger to:
          log everything to the screen
          WARNING to a rotating file

        Args:
            name: The name given to the logger
        Returns:
            logger: the logger object
        Raises:
            None
        """

# Create logger
        self._logger = logging.getLogger('mvp.'+name)
        self._logger.setLevel(lvl)
        # Rotating File handler
        fname = "/home/pi/logs/logger.log"
        if file==None:
            file_handler = TimedRotatingFileHandler(fname, when="d", interval=30, backupCount=3)
        else:            
            file_handler = TimedRotatingFileHandler(file, when="d", interval=30, backupCount=3)            
        self._logger.setLevel(lvl)        
        #Set formaat
        fmt = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        formater = logging.Formatter(fmt)
        file_handler.setFormatter(formater)
        # Screen handler - display all (DEBUG, defaults above)
        screen_handler = logging.StreamHandler()
        screen_formater = logging.Formatter("%(levelname)s - %(name)s - %(message)s")
        screen_handler.setFormatter(screen_formater)
        # Add handlers
        self._logger.addHandler(file_handler)
        self._logger.addHandler(screen_handler)

    def setLevel(self, level):
        self._logger.setLevel(level)
        
    def detail(self, msg):
        self._logger.log(Logger.DETAIL, msg)
        
    def info(self, msg):
        self._logger.info(msg)

    def debug(self, msg):
        self._logger.debug(msg)

    def error(self, msg):
        self._logger.error(msg)

def validate():
    """Test of the logger
    A light weight test, less complex that PyUnit

    Args:
        None
    Returns:
        None
    Raises:
        None
    """
    print("Test MvpLogger")
    print("Getting logger")
    logger = Logger("LogUtilTest")    
    print("Info: " + str(Logger.DETAIL))
    print("Info: " + str(Logger.INFO))
    print("Debug: " + str(Logger.DEBUG))
    print("Error: " + str(Logger.ERROR))    

    for x in Logger.lvl:
        logger.setLevel(Logger.lvl[x])
        print("Testing Level: " + str(Logger.lvl[x]))
        logger.detail("Something picky")
        logger.debug("Something happening here")
        logger.info("Just thought you might like to know")
        logger.error("Will Robinson ...")

if __name__ == "__main__":
    validate()
