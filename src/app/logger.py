import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logger():
    """
    Konfiguriert und initialisiert den Logger für die Anwendung
    """
    # Logger erstellen
    logger = logging.getLogger("user_service")
    logger.setLevel(logging.INFO)

    # Formatierung festlegen
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Datei-Handler (rotierend)
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "user_service.log"),
        maxBytes=10485760,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# Logger-Instanz für den Import
logger = setup_logger()
