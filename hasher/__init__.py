from logging import DEBUG, Formatter, StreamHandler, getLogger

logger = getLogger("hasher")
logger.setLevel(DEBUG)

formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

streamHandler = StreamHandler()
streamHandler.setLevel(DEBUG)
streamHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
