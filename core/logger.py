import logging

logger = logging.getLogger(__name__)

# handler determines what our logs go: stdout/file
shell_handler = logging.StreamHandler()
file_handler = logging.FileHandler("debug.log")

logger.setLevel(logging.DEBUG)
shell_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.DEBUG)

# formatter determines how our logs look like
fmt_shell = "%(levelsname)s %(asctime)s %(message)s"
fmt_file = (
    "%(levelsname)s %(asctime)s:[%(filename)s:%(funcName)s:%(lineno)d] %(message)s"
)

shell_formatter = logging.Formatter(fmt_shell)
file_formatter = logging.Formatter(fmt_file)

# hook all together
shell_handler.setFormatter(shell_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(shell_handler)
logger.addHandler(file_handler)

# fmt = '%(levelsname)s %(asctime)s:[%(filename)s:%(funcName)s:%(lineno)d] %(message)s'
# formatter = logging.Formatter(fmt)

# handler.setFormatter(formatter)

# logger.addHandler(handler)
# logger.setLevel(logging.DEBUG)# WARNING

# logger.debug('Debug statement')
# logger.info('Info statement')
# logger.warning('Warning statement')
# logger.critical('Critical statement')
# logger.error('Error statement')
