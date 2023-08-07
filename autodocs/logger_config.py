import logging

LOGGING_LEVEL = logging.DEBUG

logging.basicConfig(
    level=LOGGING_LEVEL,
    format=(
        "[%(asctime)s][%(levelname)s][%(name)s][%(funcName)s]"
        + "[%(filename)s:%(lineno)d] %(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Ignore logs from packages
logging.getLogger("urllib3").setLevel(logging.WARNING)