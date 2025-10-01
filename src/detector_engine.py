import os
import yaml
import json
from typing import List, Dict, Any, Optional
from pathlib import Path

from detectors.base_detector import CodeSmell
from detectors.structure_detectors import LongMethodDetector, GodClassDetector
from detectors.parameter_detectors import LargeParameterListDetector, MagicNumberDetector
from detectors.duplication_detectors import DuplicatedCodeDetector, FeatureEnvyDetector

class CodeSmellDetector:
    """Main code smell detection engine"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.detectors = self._initialize_detectors()
        self.active_detectors = []
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if config_path is None:
            # Default config path
            current_dir = Path(__file__).parent.parent
            config_path = current_dir / "config" / "config.yaml"
        
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            return self._get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default configuration"""
        return {
            'code_smells': {
                'LongMethod': {'enabled': True, 'threshold_lines': 30},
                'GodClass': {'enabled': True, 'threshold_methods': 15, 'threshold_lines': 200},
                'DuplicatedCode': {'enabled': True, 'min_duplicate_lines': 3, 'similarity_threshold': 0.8},
                'LargeParameterList': {'enabled': True, 'threshold_parameters': 5},
                'MagicNumbers': {'enabled': True, 'exclude_common': True, 'exclude_constants': True},
                'FeatureEnvy': {'enabled': True, 'external_calls_threshold': 5}
            },
            'output': {
                'format': 'detailed',
                'include_line_numbers': True,
                'include_suggestions': True
            },
            'analysis': {
                'file_extensions': ['.java'],
                'exclude_patterns': ['*Test.java', '*test.java'],
                'include_patterns': ['*.java']
            }
        }
    
    def _initialize_detectors(self) -> Dict[str, Any]:
        """Initialize all available detectors"""
        detectors = {}
        
        smell_configs = self.config.get('code_smells', {})
        
        # Initialize each detector with its configuration
        detectors['LongMethod'] = LongMethodDetector(smell_configs.get('LongMethod', {}))
        detectors['GodClass'] = GodClassDetector(smell_configs.get('GodClass', {}))
        detectors['DuplicatedCode'] = DuplicatedCodeDetector(smell_configs.get('DuplicatedCode', {}))
        detectors['LargeParameterList'] = LargeParameterListDetector(smell_configs.get('LargeParameterList', {}))
        detectors['MagicNumbers'] = MagicNumberDetector(smell_configs.get('MagicNumbers', {}))
        detectors['FeatureEnvy'] = FeatureEnvyDetector(smell_configs.get('FeatureEnvy', {}))
        
        return detectors
    
    def configure_active_detectors(self, only: Optional[List[str]] = None, exclude: Optional[List[str]] = None):
        """Configure which detectors should be active based on CLI arguments"""
        all_detector_names = list(self.detectors.keys())
        
        if only:
            # Only run specified detectors
            self.active_detectors = [name for name in only if name in self.detectors]
        elif exclude:
            # Run all except excluded detectors
            self.active_detectors = [name for name in all_detector_names if name not in exclude]
        else:
            # Use configuration file settings
            self.active_detectors = [
                name for name, detector in self.detectors.items() 
                if detector.is_enabled()
            ]
    
    def analyze_file(self, file_path: str) -> List[CodeSmell]:
        """Analyze a single file for code smells"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return []
        
        all_smells = []
        
        for detector_name in self.active_detectors:
            detector = self.detectors[detector_name]
            smells = detector.detect(file_path, content)
            all_smells.extend(smells)
        
        return all_smells
    
    def analyze_directory(self, directory_path: str) -> List[CodeSmell]:
        """Analyze all Java files in a directory"""
        all_smells = []
        extensions = self.config.get('analysis', {}).get('file_extensions', ['.java'])
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    smells = self.analyze_file(file_path)
                    all_smells.extend(smells)
        
        return all_smells
    
    def generate_report(self, smells: List[CodeSmell]) -> str:
        """Generate a report from detected code smells"""
        output_format = self.config.get('output', {}).get('format', 'detailed')
        
        if output_format == 'json':
            return self._generate_json_report(smells)
        elif output_format == 'summary':
            return self._generate_summary_report(smells)
        else:
            return self._generate_detailed_report(smells)
    
    def _generate_detailed_report(self, smells: List[CodeSmell]) -> str:
        """Generate detailed text report"""
        if not smells:
            return "No code smells detected! ✓"
        
        report = []
        report.append("=" * 60)
        report.append("CODE SMELL DETECTION REPORT")
        report.append("=" * 60)
        report.append(f"Total smells detected: {len(smells)}")
        report.append(f"Active detectors: {', '.join(self.active_detectors)}")
        report.append("")
        
        # Group smells by type
        smells_by_type = {}
        for smell in smells:
            if smell.smell_type not in smells_by_type:
                smells_by_type[smell.smell_type] = []
            smells_by_type[smell.smell_type].append(smell)
        
        for smell_type, type_smells in smells_by_type.items():
            report.append(f"🔍 {smell_type} ({len(type_smells)} occurrences)")
            report.append("-" * 40)
            
            for smell in type_smells:
                report.append(f"📁 File: {smell.file_path}")
                if smell.start_line == smell.end_line:
                    report.append(f"📍 Line: {smell.start_line}")
                else:
                    report.append(f"📍 Lines: {smell.start_line}-{smell.end_line}")
                report.append(f"⚠️  {smell.description}")
                report.append(f"🔧 Severity: {smell.severity}")
                if smell.suggestion:
                    report.append(f"💡 Suggestion: {smell.suggestion}")
                report.append("")
        
        return "\n".join(report)
    
    def _generate_summary_report(self, smells: List[CodeSmell]) -> str:
        """Generate summary report"""
        if not smells:
            return "No code smells detected! ✓"
        
        # Count by type and severity
        type_counts = {}
        severity_counts = {}
        
        for smell in smells:
            type_counts[smell.smell_type] = type_counts.get(smell.smell_type, 0) + 1
            severity_counts[smell.severity] = severity_counts.get(smell.severity, 0) + 1
        
        report = []
        report.append("CODE SMELL SUMMARY")
        report.append("=" * 30)
        report.append(f"Total: {len(smells)} smells")
        report.append("")
        
        report.append("By Type:")
        for smell_type, count in sorted(type_counts.items()):
            report.append(f"  {smell_type}: {count}")
        
        report.append("")
        report.append("By Severity:")
        for severity, count in sorted(severity_counts.items()):
            report.append(f"  {severity}: {count}")
        
        return "\n".join(report)
    
    def _generate_json_report(self, smells: List[CodeSmell]) -> str:
        """Generate JSON report"""
        report_data = {
            "total_smells": len(smells),
            "active_detectors": self.active_detectors,
            "smells": [smell.to_dict() for smell in smells]
        }
        return json.dumps(report_data, indent=2)
    
    def get_available_detectors(self) -> List[str]:
        """Get list of all available detector names"""
        return list(self.detectors.keys())