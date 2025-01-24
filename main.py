#!/usr/bin/env python3
"""
Document Indexer
---------------------------
A desktop application for document indexing and information retrieval,
built with PyQt6.

This application provides a graphical interface for:
- Loading and managing document collections
- Building and maintaining inverted indices
- Performing boolean and ranked retrieval queries
- Visualizing document statistics and index structures

Author: Matthew Branson
Course: CSC 790 Information Retrieval
Version: 0.1.0

"""

import sys
import json
import logging
import importlib.resources as resources
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QGuiApplication
from app.src.doc_indexer import DocIndexer
import signal



def load_config():
    config_path = Path("config.json")    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return json.load(f)
    else:
        default_config_str = resources.read_text("resources", "default_config.json")
        default_config = json.loads(default_config_str)
        with open(config_path, 'w') as f:
            json.dump(default_config, indent=4, fp=f)
                
        return default_config

def setup_logging(config):
    log_path = Path(config["logging"]["file_path"])
    log_path.parent.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, config["logging"]["level"]),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler(sys.stdout)
        ]
    )

def setup_signal_handling(app, window, logger):
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}. Initiating graceful shutdown...")
        window.close()
        app.quit()
    
    # Handle system termination signals
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # System termination
    # Dockable widgets may still give an ignorable flush error on hard exit

def setup_exception_hook(logger):
    def exception_hook(exctype, value, traceback):
        logger.critical("Uncaught exception:", exc_info=(exctype, value, traceback))
        sys.__excepthook__(exctype, value, traceback)  # Call the default handler
    sys.excepthook = exception_hook

def main():
    config = load_config()
    setup_logging(config)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Information Retrieval System")
        
        # Configure High DPI settings based on config
        # Not really important now but will be good to have when doing visualizations later
        # The changes to policies in PyQt6 are like half the battle
        if config["display"]["enable_high_dpi"]:
            QApplication.setHighDpiScaleFactorRoundingPolicy(
                QGuiApplication.highDpiScaleFactorRoundingPolicy()
            )
        
        app = QApplication(sys.argv)
        app.setApplicationName(config["application"]["name"])
        app.setApplicationVersion(config["application"]["version"])
        
        window = DocIndexer(config)
        setup_signal_handling(app, window, logger)
        setup_exception_hook(logger)
        
        window.show()
        return app.exec()
        
    except Exception as e:
        logger.error(f"Application failed to start: {e}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main())