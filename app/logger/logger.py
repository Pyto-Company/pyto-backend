import logging
from datetime import datetime
import os

# Créer le dossier logs s'il n'existe pas
log_directory = "../logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Définir le nom du fichier de log avec la date
log_filename = os.path.join(log_directory, f"pyto-{datetime.now().strftime('%Y-%m-%d')}.log")

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename),  # Log dans un fichier daté
        logging.StreamHandler()  # Log aussi dans la console
    ]
)

# Créer le logger
logger = logging.getLogger("Pyto API")