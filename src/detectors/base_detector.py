from abc import ABC, abstractmethod
from typing import List, Dict, Any
import re

class CodeSmell:
    """Represents a detected code smell"""
    def __init__(self, smell_type: str, file_path: str, start_line: int, end_line: int, 
                 description: str, severity: str = "Medium", suggestion: str = ""):
        self.smell_type = smell_type
        self.file_path = file_path
        self.start_line = start_line
        self.end_line = end_line
        self.description = description
        self.severity = severity
        self.suggestion = suggestion
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.smell_type,
            "file": self.file_path,
            "start_line": self.start_line,
            "end_line": self.end_line,
            "description": self.description,
            "severity": self.severity,
            "suggestion": self.suggestion
        }

class BaseDetector(ABC):
    """Abstract base class for code smell detectors"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get('enabled', True)
    
    @abstractmethod
    def detect(self, file_path: str, content: str) -> List[CodeSmell]:
        """Detect code smells in the given file content"""
        pass
    
    @property
    @abstractmethod
    def smell_type(self) -> str:
        """Return the type of code smell this detector finds"""
        pass
    
    def is_enabled(self) -> bool:
        return self.enabled
    
    def _count_lines(self, text: str) -> int:
        """Count non-empty lines in text"""
        return len([line for line in text.split('\n') if line.strip()])
    
    def _extract_methods(self, content: str) -> List[Dict[str, Any]]:
        """Extract method information from Java code"""
        methods = []
        lines = content.split('\n')
        
        # Improved regex for Java method declarations
        method_pattern = r'^\s*(public|private|protected)?\s*(static)?\s*(final)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*\{?'
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if re.search(method_pattern, line):
                method_match = re.search(method_pattern, line)
                if method_match:
                    method_name = method_match.group(4)
                    start_line = i + 1
                    
                    # Find method end by counting braces
                    brace_count = line.count('{') - line.count('}')
                    j = i + 1
                    method_lines = [line]
                    
                    while j < len(lines) and brace_count > 0:
                        current_line = lines[j]
                        method_lines.append(current_line)
                        brace_count += current_line.count('{') - current_line.count('}')
                        j += 1
                    
                    end_line = j
                    method_content = '\n'.join(method_lines)
                    
                    # Count parameters
                    param_match = re.search(r'\(([^)]*)\)', line)
                    param_count = 0
                    if param_match and param_match.group(1).strip():
                        params = param_match.group(1).split(',')
                        param_count = len([p for p in params if p.strip()])
                    
                    methods.append({
                        'name': method_name,
                        'start_line': start_line,
                        'end_line': end_line,
                        'content': method_content,
                        'line_count': self._count_lines(method_content),
                        'parameter_count': param_count
                    })
                    
                    i = j
                else:
                    i += 1
            else:
                i += 1
        
        return methods
    
    def _extract_classes(self, content: str) -> List[Dict[str, Any]]:
        """Extract class information from Java code"""
        classes = []
        lines = content.split('\n')
        
        class_pattern = r'^\s*(public|private|protected)?\s*class\s+(\w+)'
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            class_match = re.search(class_pattern, line)
            if class_match:
                class_name = class_match.group(2)
                start_line = i + 1
                
                # Find class end by counting braces
                brace_count = line.count('{') - line.count('}')
                j = i + 1
                class_lines = [line]
                
                while j < len(lines) and brace_count > 0:
                    current_line = lines[j]
                    class_lines.append(current_line)
                    brace_count += current_line.count('{') - current_line.count('}')
                    j += 1
                
                end_line = j
                class_content = '\n'.join(class_lines)
                
                # Count methods in class
                methods = self._extract_methods(class_content)
                
                classes.append({
                    'name': class_name,
                    'start_line': start_line,
                    'end_line': end_line,
                    'content': class_content,
                    'line_count': self._count_lines(class_content),
                    'method_count': len(methods),
                    'methods': methods
                })
                
                i = j
            else:
                i += 1
        
        return classes