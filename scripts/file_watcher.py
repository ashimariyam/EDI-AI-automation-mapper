"""
File watcher module for monitoring input directory for new EDI files.
"""

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from loguru import logger

class EDIFileHandler(FileSystemEventHandler):
    def __init__(self, file_processor, mapping_engine, output_dir):
        self.file_processor = file_processor
        self.mapping_engine = mapping_engine
        self.output_dir = Path(output_dir)
    
    def on_created(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            logger.info(f"New file detected: {file_path}")
            
            try:
                # Process the file
                processed_data = self.file_processor.process_file(file_path)
                
                # Generate mappings
                mappings = self.mapping_engine.generate_mappings(processed_data)
                
                # Save the output
                output_file = self.output_dir / f"{file_path.stem}_mapping.json"
                self.mapping_engine.save_mappings(mappings, output_file)
                
                logger.info(f"Successfully processed and mapped {file_path}")
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")

class FileWatcher:
    def __init__(self, input_dir, output_dir, file_processor, mapping_engine):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.file_processor = file_processor
        self.mapping_engine = mapping_engine
        
        # Initialize the observer
        self.observer = Observer()
        self.event_handler = EDIFileHandler(
            file_processor=self.file_processor,
            mapping_engine=self.mapping_engine,
            output_dir=self.output_dir
        )
    
    def start(self):
        """Start watching the input directory for new files."""
        logger.info(f"Starting file watcher for directory: {self.input_dir}")
        self.observer.schedule(
            self.event_handler,
            str(self.input_dir),
            recursive=False
        )
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            logger.info("File watcher stopped")
        
        self.observer.join() 