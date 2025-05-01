"""
File processor module for handling different file types and extracting EDI information.
"""

import pdfplumber
from pathlib import Path
from typing import Dict, Any
import pandas as pd
from loguru import logger

class FileProcessor:
    def __init__(self):
        self.supported_extensions = {
            '.edi': self._process_edi,
            '.pdf': self._process_pdf,
            '.csv': self._process_csv
        }
    
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Process a file based on its extension and return extracted data.
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            Dictionary containing processed data
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()
        
        if extension not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {extension}")
        
        logger.info(f"Processing file: {file_path}")
        return self.supported_extensions[extension](file_path)
    
    def _process_edi(self, file_path: Path) -> Dict[str, Any]:
        """Process EDI files (X12, EDIFACT)."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic EDI parsing - this will need to be enhanced based on specific EDI formats
        segments = content.split('~')
        processed_data = {
            'file_type': 'edi',
            'segments': [],
            'fields': {}
        }
        
        for segment in segments:
            if not segment.strip():
                continue
                
            elements = segment.split('*')
            segment_id = elements[0]
            
            processed_data['segments'].append({
                'id': segment_id,
                'elements': elements[1:]
            })
            
            # Store specific fields of interest
            if segment_id == 'BEG':
                processed_data['fields']['BEG03'] = elements[3] if len(elements) > 3 else None
            elif segment_id == 'PO1':
                processed_data['fields']['PO1'] = elements[1:] if len(elements) > 1 else None
        
        return processed_data
    
    def _process_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Process PDF files to extract specifications."""
        processed_data = {
            'file_type': 'pdf',
            'text': '',
            'tables': []
        }
        
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                # Extract text
                processed_data['text'] += page.extract_text() or ''
                
                # Extract tables
                tables = page.extract_tables()
                if tables:
                    processed_data['tables'].extend(tables)
        
        return processed_data
    
    def _process_csv(self, file_path: Path) -> Dict[str, Any]:
        """Process CSV files."""
        df = pd.read_csv(file_path)
        return {
            'file_type': 'csv',
            'columns': df.columns.tolist(),
            'data': df.to_dict(orient='records')
        } 