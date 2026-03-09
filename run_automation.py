#!/usr/bin/env python3
"""
Script para ejecutar la automatización en EC2 con logging.
Se ejecuta vía cron job diariamente.
"""

import sys
import os
import logging
from datetime import datetime

# Configurar logging
log_dir = os.path.expanduser("~/castillo_logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"castillo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

try:
    logger.info("=" * 60)
    logger.info("Iniciando automatización Castillo Chancay")
    logger.info(f"Hora de inicio: {datetime.now()}")
    logger.info("=" * 60)
    
    # Importar el main
    from main import main
    
    # Ejecutar
    main()
    
    logger.info("=" * 60)
    logger.info("✅ Automatización completada exitosamente")
    logger.info(f"Hora de término: {datetime.now()}")
    logger.info("=" * 60)
    
except Exception as e:
    logger.error("=" * 60)
    logger.error(f"❌ Error en la automatización: {str(e)}")
    logger.error(f"Hora del error: {datetime.now()}")
    logger.error("=" * 60, exc_info=True)
    sys.exit(1)
