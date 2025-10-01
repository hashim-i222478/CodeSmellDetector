# Code Smell Detector

A Python-based tool for detecting common code smells in Java source files. This tool can identify and report on six major code smell patterns that indicate potential issues with code maintainability and design.

## Features

✨ **Detects 6 Major Code Smells:**
- **Long Method** - Methods that are excessively long
- **God Class (Blob)** - Classes with too many responsibilities 
- **Duplicated Code** - Repeated code blocks that should be refactored
- **Large Parameter List** - Methods with too many parameters
- **Magic Numbers** - Hardcoded numeric values that should be constants
- **Feature Envy** - Methods overly interested in other classes' data

🔧 **Flexible Configuration:**
- YAML-based configuration with per-smell settings
- CLI overrides for runtime control
- Adjustable thresholds and detection parameters

📊 **Multiple Output Formats:**
- Detailed reports with line numbers and suggestions
- Summary reports with statistics
- JSON output for integration with other tools

## Installation

### Prerequisites
- Python 3.7+
- PyYAML package

### Setup
```bash
# Install required dependencies
pip install PyYAML

# Clone or download the project
cd code-smell-detector/src
```

## Usage

### Basic Usage
```bash
# Analyze a single file
python detector_cli.py MyClass.java

# Analyze all Java files in a directory
python detector_cli.py src/

# List available detectors
python detector_cli.py --list-detectors
```

### Advanced Usage

#### Selective Detection
```bash
# Only detect specific smells
python detector_cli.py src/ --only LongMethod,GodClass

# Exclude specific smells
python detector_cli.py src/ --exclude MagicNumbers,DuplicatedCode
```

#### Output Formats
```bash
# Detailed report (default)
python detector_cli.py src/ --format detailed

# Summary statistics
python detector_cli.py src/ --format summary

# JSON output
python detector_cli.py src/ --format json
```

#### Configuration
```bash
# Use custom configuration file
python detector_cli.py src/ --config custom_config.yaml

# Save report to file
python detector_cli.py src/ --output report.txt

# Verbose output
python detector_cli.py src/ --verbose
```

## Configuration

The tool uses a YAML configuration file (`config/config.yaml`) to customize detection parameters:

```yaml
code_smells:
  LongMethod:
    enabled: true
    threshold_lines: 30
  
  GodClass:
    enabled: true
    threshold_methods: 15
    threshold_lines: 200
  
  MagicNumbers:
    enabled: true
    exclude_common: true  # Skip 0, 1, -1, 2, etc.
    exclude_constants: true  # Skip final/static variables
```

### CLI Precedence
- `--only` overrides everything else
- `--exclude` overrides config file
- Config file settings used as default

## Code Smell Descriptions

### 1. Long Method
**What it detects:** Methods longer than the configured threshold (default: 30 lines)
**Why it matters:** Long methods are harder to understand, test, and maintain
**Suggestion:** Break into smaller, focused methods

### 2. God Class (Blob)
**What it detects:** Classes with too many methods or lines of code
**Why it matters:** Violates Single Responsibility Principle
**Suggestion:** Split into multiple smaller, focused classes

### 3. Duplicated Code
**What it detects:** Similar code blocks that appear multiple times
**Why it matters:** Changes must be made in multiple places
**Suggestion:** Extract into reusable methods

### 4. Large Parameter List
**What it detects:** Methods with many parameters (default: >5)
**Why it matters:** Hard to use and understand
**Suggestion:** Use parameter objects or builder pattern

### 5. Magic Numbers
**What it detects:** Hardcoded numeric values in code
**Why it matters:** Unclear meaning and hard to maintain
**Suggestion:** Extract into named constants

### 6. Feature Envy
**What it detects:** Methods that access other classes' data frequently
**Why it matters:** Suggests misplaced responsibility
**Suggestion:** Move method to appropriate class

## Example Output

### Detailed Report
```
============================================================
CODE SMELL DETECTION REPORT
============================================================
Total smells detected: 51
Active detectors: LongMethod, GodClass, DuplicatedCode, LargeParameterList, MagicNumbers, FeatureEnvy

🔍 LongMethod (1 occurrences)
----------------------------------------
📁 File: LibrarySystem.java
📍 Lines: 32-122
⚠️  Method 'borrowBook' is too long (90 lines, threshold: 30)
🔧 Severity: High
💡 Suggestion: Consider breaking this method into smaller, more focused methods
```

### Summary Report
```
CODE SMELL SUMMARY
==============================
Total: 94 smells

By Type:
  FeatureEnvy: 7
  GodClass: 2
  LongMethod: 3
  MagicNumbers: 82

By Severity:
  High: 3
  Low: 82
  Medium: 9
```

## Project Structure

```
code-smell-detector/
├── src/
│   ├── detector_cli.py           # Command-line interface
│   ├── detector_engine.py        # Main detection engine
│   └── detectors/
│       ├── base_detector.py      # Abstract base class
│       ├── structure_detectors.py # Long Method, God Class
│       ├── parameter_detectors.py # Large Parameter List, Magic Numbers
│       └── duplication_detectors.py # Duplicated Code, Feature Envy
├── config/
│   └── config.yaml              # Configuration file
├── test-files/                  # Sample Java files for testing
└── README.md                    # This documentation
```

## Testing

The detector has been tested on a deliberately smelly Java library management system that contains all six code smell types. Test results show accurate detection and reporting.

### Sample Test Commands
```bash
# Test all detectors on sample code
python detector_cli.py ../test-files/ --verbose

# Test specific detectors
python detector_cli.py ../test-files/LibrarySystem.java --only LongMethod,GodClass

# Generate JSON report
python detector_cli.py ../test-files/ --format json --output results.json
```

## Extension Points

The tool is designed for extensibility:

1. **Add New Detectors:** Inherit from `BaseDetector` and implement the detection logic
2. **Custom Output Formats:** Extend the reporting system in `detector_engine.py`
3. **Language Support:** Adapt the parsing logic for other programming languages
4. **IDE Integration:** Use the JSON output format for integration with development tools

## Contributing

To add a new code smell detector:

1. Create a new detector class inheriting from `BaseDetector`
2. Implement the `detect()` method and `smell_type` property
3. Add configuration options to `config.yaml`
4. Register the detector in `detector_engine.py`
5. Update documentation

## License

This project is created for educational purposes as part of a Software Engineering assignment demonstrating code smell detection techniques.