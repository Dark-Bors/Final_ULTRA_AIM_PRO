# utilities.py
# This file contains utility functions like performance metrics.

import tkinter as tk
from PIL import Image, ImageTk
from app_logging import logger

def load_image(path, size=None):
    try:
        image = Image.open(path)
        if size:
            image = image.resize(size, Image.ANTIALIAS)
        logger.info(f"ℹ️ Image loaded successfully from {path}")  # Log an info message
        return ImageTk.PhotoImage(image)
    except Exception as e:
        logger.critical(f"⛔ Critical error loading image from {path}: {e}", exc_info=True)  # Log a critical error message
        raise