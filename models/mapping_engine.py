"""
Mapping engine module for suggesting mappings between EDI fields and ERP fields.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from loguru import logger

class MappingEngine:
    def __init__(self):
        # Initialize the sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load ERP field definitions (to be populated with actual ERP field data)
        self.erp_fields = self._load_erp_fields()
        
        # Pre-compute embeddings for ERP fields
        self.erp_embeddings = self._compute_erp_embeddings()
    
    def _load_erp_fields(self) -> Dict[str, Dict[str, Any]]:
        """Load ERP field definitions."""
        # This is a placeholder - in a real implementation, this would load from a database or file
        return {
            'SAP': {
                'E1EDK01': {'description': 'Document header', 'fields': ['BELNR', 'BUKRS', 'LIFNR']},
                'E1EDP01': {'description': 'Item data', 'fields': ['MATNR', 'MENGE', 'MEINS']}
            },
            'Oracle': {
                'PO_HEADER': {'description': 'Purchase Order Header', 'fields': ['PO_NUMBER', 'VENDOR_ID', 'ORDER_DATE']},
                'PO_LINE': {'description': 'Purchase Order Line', 'fields': ['ITEM_NUMBER', 'QUANTITY', 'UOM']}
            }
        }
    
    def _compute_erp_embeddings(self) -> Dict[str, np.ndarray]:
        """Compute embeddings for all ERP fields."""
        embeddings = {}
        for erp_system, segments in self.erp_fields.items():
            for segment_id, segment_info in segments.items():
                # Create a description that combines segment ID and description
                text = f"{segment_id}: {segment_info['description']}"
                embeddings[segment_id] = self.model.encode(text)
        return embeddings
    
    def generate_mappings(self, processed_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate mappings between EDI fields and ERP fields.
        
        Args:
            processed_data: Dictionary containing processed EDI data
            
        Returns:
            Dictionary containing suggested mappings
        """
        mappings = {
            'source_file': processed_data.get('file_type', 'unknown'),
            'mappings': []
        }
        
        if processed_data['file_type'] == 'edi':
            # Process EDI segments
            for segment in processed_data['segments']:
                segment_id = segment['id']
                segment_text = f"{segment_id}: {' '.join(segment['elements'])}"
                
                # Compute embedding for the segment
                segment_embedding = self.model.encode(segment_text)
                
                # Find best matching ERP segment
                best_match = self._find_best_match(segment_embedding)
                
                if best_match:
                    mappings['mappings'].append({
                        'edi_segment': segment_id,
                        'erp_segment': best_match['segment_id'],
                        'confidence': best_match['similarity'],
                        'suggested_mappings': self._suggest_field_mappings(segment, best_match['segment_id'])
                    })
        
        return mappings
    
    def _find_best_match(self, segment_embedding: np.ndarray) -> Dict[str, Any]:
        """Find the best matching ERP segment for a given EDI segment."""
        best_match = None
        max_similarity = 0.0
        
        for segment_id, erp_embedding in self.erp_embeddings.items():
            similarity = cosine_similarity(
                segment_embedding.reshape(1, -1),
                erp_embedding.reshape(1, -1)
            )[0][0]
            
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = {
                    'segment_id': segment_id,
                    'similarity': float(similarity)
                }
        
        return best_match if max_similarity > 0.5 else None
    
    def _suggest_field_mappings(self, edi_segment: Dict[str, Any], erp_segment_id: str) -> List[Dict[str, Any]]:
        """Suggest field-level mappings between EDI and ERP segments."""
        suggestions = []
        
        # Get ERP fields for the segment
        erp_fields = None
        for erp_system, segments in self.erp_fields.items():
            if erp_segment_id in segments:
                erp_fields = segments[erp_segment_id]['fields']
                break
        
        if not erp_fields:
            return suggestions
        
        # Create simple 1:1 mapping suggestions
        for i, element in enumerate(edi_segment['elements']):
            if i < len(erp_fields):
                suggestions.append({
                    'edi_field': f"{edi_segment['id']}_{i+1}",
                    'erp_field': erp_fields[i],
                    'confidence': 0.8  # This would be computed based on field similarity in a real implementation
                })
        
        return suggestions
    
    def save_mappings(self, mappings: Dict[str, Any], output_path: Path):
        """Save the generated mappings to a file."""
        with open(output_path, 'w') as f:
            json.dump(mappings, f, indent=2)
        logger.info(f"Saved mappings to {output_path}") 