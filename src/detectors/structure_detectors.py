from typing import List
from .base_detector import BaseDetector, CodeSmell

class LongMethodDetector(BaseDetector):
    """Detects methods that are too long"""
    
    @property
    def smell_type(self) -> str:
        return "LongMethod"
    
    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        threshold = self.config.get('threshold_lines', 30)
        
        methods = self._extract_methods(content)
        
        for method in methods:
            if method['line_count'] > threshold:
                smell = CodeSmell(
                    smell_type=self.smell_type,
                    file_path=file_path,
                    start_line=method['start_line'],
                    end_line=method['end_line'],
                    description=f"Method '{method['name']}' is too long ({method['line_count']} lines, threshold: {threshold})",
                    severity="High" if method['line_count'] > threshold * 2 else "Medium",
                    suggestion="Consider breaking this method into smaller, more focused methods"
                )
                smells.append(smell)
        
        return smells

class GodClassDetector(BaseDetector):
    """Detects classes that have too many responsibilities (God/Blob classes)"""
    
    @property
    def smell_type(self) -> str:
        return "GodClass"
    
    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        smells = []
        method_threshold = self.config.get('threshold_methods', 15)
        line_threshold = self.config.get('threshold_lines', 200)
        
        classes = self._extract_classes(content)
        
        for cls in classes:
            violations = []
            
            if cls['method_count'] > method_threshold:
                violations.append(f"too many methods ({cls['method_count']} > {method_threshold})")
            
            if cls['line_count'] > line_threshold:
                violations.append(f"too many lines ({cls['line_count']} > {line_threshold})")
            
            if violations:
                smell = CodeSmell(
                    smell_type=self.smell_type,
                    file_path=file_path,
                    start_line=cls['start_line'],
                    end_line=cls['end_line'],
                    description=f"Class '{cls['name']}' is a God/Blob class: {', '.join(violations)}",
                    severity="High",
                    suggestion="Consider breaking this class into multiple smaller, more focused classes"
                )
                smells.append(smell)
        
        return smells