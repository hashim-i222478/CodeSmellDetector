from typing import List
import re
from .base_detector import BaseDetector, CodeSmell

class LargeParameterListDetector(BaseDetector):
    """Detects methods with too many parameters"""
    
    @property
    def smell_type(self) -> str:
        return "LargeParameterList"
    
    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        threshold = self.config.get('threshold_parameters', 5)
        
        methods = self._extract_methods(content)
        
        for method in methods:
            if method['parameter_count'] > threshold:
                smell = CodeSmell(
                    smell_type=self.smell_type,
                    file_path=file_path,
                    start_line=method['start_line'],
                    end_line=method['start_line'],  # Just highlight the method signature
                    description=f"Method '{method['name']}' has too many parameters ({method['parameter_count']} > {threshold})",
                    severity="Medium",
                    suggestion="Consider using parameter objects or builder pattern to reduce parameter count"
                )
                smells.append(smell)
        
        return smells

class MagicNumberDetector(BaseDetector):
    """Detects magic numbers in code"""
    
    @property
    def smell_type(self) -> str:
        return "MagicNumbers"
    
    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        exclude_common = self.config.get('exclude_common', True)
        exclude_constants = self.config.get('exclude_constants', True)
        
        lines = content.split('\n')
        
        # Common numbers to exclude if exclude_common is True
        common_numbers = {0, 1, -1, 2, 10, 100, 1000} if exclude_common else set()
        
        # Pattern to find numeric literals
        number_pattern = r'\b(\d+\.?\d*)\b'
        
        for line_num, line in enumerate(lines, 1):
            # Skip constant declarations if exclude_constants is True
            if exclude_constants and re.search(r'(final|static|const)\s+.*=', line, re.IGNORECASE):
                continue
            
            # Skip comments
            if line.strip().startswith('//') or line.strip().startswith('/*') or line.strip().startswith('*'):
                continue
            
            # Find all numbers in the line
            for match in re.finditer(number_pattern, line):
                try:
                    number = float(match.group(1))
                    
                    # Skip common numbers
                    if number in common_numbers:
                        continue
                    
                    # Skip array indices and loop counters (basic heuristic)
                    context = line[max(0, match.start()-10):match.end()+10]
                    if re.search(r'\[\s*\d+\s*\]|for\s*\(.*\d+.*\)', context):
                        continue
                    
                    smell = CodeSmell(
                        smell_type=self.smell_type,
                        file_path=file_path,
                        start_line=line_num,
                        end_line=line_num,
                        description=f"Magic number '{number}' found at line {line_num}",
                        severity="Low",
                        suggestion="Consider extracting this number into a named constant"
                    )
                    smells.append(smell)
                    
                except ValueError:
                    continue
        
        return smells