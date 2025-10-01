#!/usr/bin/env python3
"""
Code Smell Detector CLI
Detects code smells in Java source files
"""

import argparse
import sys
import os
from pathlib import Path
from detector_engine import CodeSmellDetector

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Detect code smells in Java source files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python detector_cli.py src/                        # Analyze all Java files in src/
  python detector_cli.py MyClass.java               # Analyze single file
  python detector_cli.py src/ --only LongMethod     # Only detect long methods
  python detector_cli.py src/ --exclude MagicNumbers # Exclude magic number detection
  python detector_cli.py src/ --format json         # Output in JSON format
  python detector_cli.py src/ --config my_config.yaml # Use custom config
        """
    )
    
    parser.add_argument(
        'target',
        nargs='?',
        help='File or directory to analyze'
    )
    
    parser.add_argument(
        '--only',
        type=str,
        help='Only run specified detectors (comma-separated). Overrides config. Available: LongMethod,GodClass,DuplicatedCode,LargeParameterList,MagicNumbers,FeatureEnvy'
    )
    
    parser.add_argument(
        '--exclude',
        type=str,
        help='Exclude specified detectors (comma-separated). Overrides config.'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='Path to configuration file (default: config/config.yaml)'
    )
    
    parser.add_argument(
        '--format',
        choices=['detailed', 'summary', 'json'],
        default='detailed',
        help='Output format (default: detailed)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Output file (default: print to stdout)'
    )
    
    parser.add_argument(
        '--list-detectors',
        action='store_true',
        help='List all available detectors and exit'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()

def parse_detector_list(detector_string):
    """Parse comma-separated detector names"""
    if not detector_string:
        return None
    return [detector.strip() for detector in detector_string.split(',')]

def validate_detectors(detector_names, available_detectors):
    """Validate that detector names are valid"""
    if not detector_names:
        return True
    
    invalid_detectors = [name for name in detector_names if name not in available_detectors]
    if invalid_detectors:
        print(f"Error: Invalid detector names: {', '.join(invalid_detectors)}")
        print(f"Available detectors: {', '.join(available_detectors)}")
        return False
    return True

def main():
    """Main CLI function"""
    args = parse_arguments()
    
    try:
        # Initialize detector engine
        detector = CodeSmellDetector(args.config)
        
        # List detectors if requested
        if args.list_detectors:
            available = detector.get_available_detectors()
            print("Available Code Smell Detectors:")
            print("=" * 35)
            for detector_name in available:
                config = detector.config.get('code_smells', {}).get(detector_name, {})
                enabled = config.get('enabled', True)
                status = "✓ enabled" if enabled else "✗ disabled"
                print(f"  {detector_name:<20} {status}")
            return 0
        
        # Validate target is provided for analysis
        if not args.target:
            print("Error: Target file or directory is required for analysis")
            return 1
        
        # Validate target exists
        if not os.path.exists(args.target):
            print(f"Error: Target '{args.target}' does not exist")
            return 1
        
        # Parse detector lists
        only_detectors = parse_detector_list(args.only)
        exclude_detectors = parse_detector_list(args.exclude)
        
        # Validate detector names
        available_detectors = detector.get_available_detectors()
        if not validate_detectors(only_detectors, available_detectors):
            return 1
        if not validate_detectors(exclude_detectors, available_detectors):
            return 1
        
        # Configure active detectors
        detector.configure_active_detectors(only=only_detectors, exclude=exclude_detectors)
        
        if args.verbose:
            print(f"Analyzing: {args.target}")
            print(f"Active detectors: {', '.join(detector.active_detectors)}")
            print()
        
        # Analyze target
        if os.path.isfile(args.target):
            smells = detector.analyze_file(args.target)
        else:
            smells = detector.analyze_directory(args.target)
        
        # Override output format if specified
        if args.format:
            detector.config['output']['format'] = args.format
        
        # Generate report
        report = detector.generate_report(smells)
        
        # Output report
        if args.output:
            try:
                with open(args.output, 'w') as f:
                    f.write(report)
                print(f"Report written to: {args.output}")
            except Exception as e:
                print(f"Error writing to file: {e}")
                return 1
        else:
            print(report)
        
        return 0
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())