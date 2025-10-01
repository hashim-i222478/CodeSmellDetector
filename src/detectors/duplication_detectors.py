from typing import List, Set, Tuple
import re
from difflib import SequenceMatcher
from .base_detector import BaseDetector, CodeSmell

class DuplicatedCodeDetector(BaseDetector):
    """Detects duplicated code blocks"""
    
    @property
    def smell_type(self) -> str:
        return "DuplicatedCode"
    
    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        min_lines = self.config.get('min_duplicate_lines', 3)
        similarity_threshold = self.config.get('similarity_threshold', 0.8)
        
        lines = content.split('\n')
        # Remove empty lines and comments for comparison
        code_lines = []
        line_mapping = []
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
                code_lines.append(stripped)
                line_mapping.append(i + 1)  # 1-based line numbers
        
        # Find duplicated blocks
        duplicates = self._find_duplicates(code_lines, line_mapping, min_lines, similarity_threshold)
        
        for duplicate in duplicates:
            smell = CodeSmell(
                smell_type=self.smell_type,
                file_path=file_path,
                start_line=duplicate['start_line'],
                end_line=duplicate['end_line'],
                description=f"Duplicated code block found (lines {duplicate['start_line']}-{duplicate['end_line']} similar to lines {duplicate['similar_start']}-{duplicate['similar_end']})",
                severity="Medium",
                suggestion="Extract this duplicated code into a reusable method"
            )
            smells.append(smell)
        
        return smells
    
    def _find_duplicates(self, lines: List[str], line_mapping: List[int], min_lines: int, threshold: float) -> List[dict]:
        duplicates = []
        processed_blocks = set()
        
        for i in range(len(lines) - min_lines + 1):
            block1 = lines[i:i + min_lines]
            block1_key = tuple(block1)
            
            if block1_key in processed_blocks:
                continue
            
            for j in range(i + min_lines, len(lines) - min_lines + 1):
                block2 = lines[j:j + min_lines]
                
                similarity = self._calculate_similarity(block1, block2)
                if similarity >= threshold:
                    duplicates.append({
                        'start_line': line_mapping[i],
                        'end_line': line_mapping[i + min_lines - 1],
                        'similar_start': line_mapping[j],
                        'similar_end': line_mapping[j + min_lines - 1],
                        'similarity': similarity
                    })
                    processed_blocks.add(block1_key)
                    break
        
        return duplicates
    
    def _calculate_similarity(self, block1: List[str], block2: List[str]) -> float:
        """Calculate similarity between two code blocks"""
        if len(block1) != len(block2):
            return 0.0
        
        total_similarity = 0.0
        for line1, line2 in zip(block1, block2):
            similarity = SequenceMatcher(None, line1, line2).ratio()
            total_similarity += similarity
        
        return total_similarity / len(block1)

class FeatureEnvyDetector(BaseDetector):
    """Detects methods that are more interested in other classes than their own"""
    
    @property
    def smell_type(self) -> str:
        return "FeatureEnvy"
    
    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        threshold = self.config.get('external_calls_threshold', 5)
        
        classes = self._extract_classes(content)
        
        for cls in classes:
            for method in cls['methods']:
                external_calls = self._count_external_calls(method['content'], cls['name'])
                
                if external_calls > threshold:
                    smell = CodeSmell(
                        smell_type=self.smell_type,
                        file_path=file_path,
                        start_line=method['start_line'],
                        end_line=method['end_line'],
                        description=f"Method '{method['name']}' shows feature envy ({external_calls} external calls > {threshold})",
                        severity="Medium",
                        suggestion="Consider moving this method to the class it's most interested in, or refactor to reduce dependencies"
                    )
                    smells.append(smell)
        
        return smells
    
    def _count_external_calls(self, method_content: str, current_class: str) -> int:
        """Count calls to external classes/objects"""
        external_calls = 0
        
        # Patterns for method calls on external objects
        patterns = [
            r'(\w+)\.(\w+)\(',  # object.method()
            r'(\w+)\.get(\w+)\(',  # object.getProperty()
            r'(\w+)\.set(\w+)\(',  # object.setProperty()
        ]
        
        lines = method_content.split('\n')
        for line in lines:
            for pattern in patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    object_name = match[0]
                    # Skip calls to 'this', 'super', or current class
                    if object_name not in ['this', 'super', current_class.lower(), 'System']:
                        # Skip local variables that are likely primitives
                        if not re.match(r'^(i|j|k|count|index|temp|result)$', object_name):
                            external_calls += 1
        
        return external_calls