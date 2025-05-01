#!/usr/bin/env python3
"""
EDI-AI Automation Mapper
Main entry point for the EDI processing and mapping automation system.
"""

import os
import logging
from pathlib import Path
from loguru import logger

from scripts.file_watcher import FileWatcher
from scripts.file_processor import FileProcessor
from models.mapping_engine import MappingEngine

# Configure logging
logger.add("logs/edi_automation.log", rotation="1 day", retention="7 days")

class EDIAutomationMapper:
    def __init__(self):
        # Initialize paths
        self.base_dir = Path(__file__).parent
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "output"
        
        # Create necessary directories
        self._setup_directories()
        
        # Initialize components
        self.file_processor = FileProcessor()
        self.mapping_engine = MappingEngine()
        self.file_watcher = FileWatcher(
            input_dir=self.input_dir,
            output_dir=self.output_dir,
            file_processor=self.file_processor,
            mapping_engine=self.mapping_engine
        )
    
    def _setup_directories(self):
        """Create necessary directories if they don't exist."""
        directories = [
            self.input_dir,
            self.output_dir,
            self.base_dir / "models",
            self.base_dir / "scripts",
            self.base_dir / "logs"
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            logger.info(f"Ensured directory exists: {directory}")
    
    def start(self):
        """Start the EDI automation system."""
        logger.info("Starting EDI Automation Mapper")
        try:
            self.file_watcher.start()
        except KeyboardInterrupt:
            logger.info("Shutting down EDI Automation Mapper")
        except Exception as e:
            logger.error(f"Error in EDI Automation Mapper: {str(e)}")
            raise

if __name__ == "__main__":
    app = EDIAutomationMapper()
    app.start() 