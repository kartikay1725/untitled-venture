import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("ideaforge")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("app.log", maxBytes=10_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)