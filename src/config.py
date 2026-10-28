import os

# Carpeta del proyecto: sube dos niveles desde este archivo (src/config.py -> dowland_videos)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carpeta donde se guardan (y se buscan) las descargas
DESCARGAS_DIR = os.path.join(BASE_DIR, "descargas")
