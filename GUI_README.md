# Code Smell Detector GUI

A user-friendly graphical interface for detecting code smells in Java source files.

## 🚀 Quick Start

### Method: Direct Execution
```bash
cd code-smell-detector/src
python detector_gui.py
```

## 🎯 GUI Features

### 📁 **File Analysis Tab**
- **File Selection:**
  - Select single Java files or entire directories
  - View selected files in an organized list
  - Clear selection with one click

- **Detection Settings:**
  - Choose detection mode: All Enabled, Only Selected, or Exclude Selected
  - Enable/disable specific code smell detectors
  - Select output format: Detailed, Summary, or JSON

- **Analysis Controls:**
  - Start analysis with progress tracking
  - Save reports to files
  - Copy results to clipboard

### ⚙️ **Configuration Tab**
- **Live Configuration Editor:**
  - Edit YAML configuration directly in the GUI
  - Load/save custom configuration files
  - Reset to default settings
  - Apply changes without restarting

- **Configurable Options:**
  - Detection thresholds for each smell type
  - Enable/disable specific detectors
  - Output formatting preferences
  - File inclusion/exclusion patterns

### 📊 **Results Tab**
- **Comprehensive Reports:**
  - Detailed analysis with line numbers and suggestions
  - Summary statistics by smell type and severity
  - JSON output for integration with other tools

- **Results Management:**
  - Clear results display
  - Export to various formats
  - Copy to clipboard functionality

### ❓ **Help Tab**
- **Complete Documentation:**
  - Overview of all code smell types
  - Step-by-step usage instructions
  - Configuration guide
  - Tips for best results

## 🔍 **Supported Code Smells**

| Code Smell | Description | Default Threshold |
|------------|-------------|------------------|
| **Long Method** | Methods that are too long | 30 lines |
| **God Class** | Classes with too many responsibilities | 15 methods / 200 lines |
| **Duplicated Code** | Repeated code blocks | 3+ similar lines |
| **Large Parameter List** | Methods with too many parameters | 5+ parameters |
| **Magic Numbers** | Hardcoded numeric values | All except 0,1,2 |
| **Feature Envy** | Methods interested in other classes | 5+ external calls |

## 🎛️ **GUI Controls**

### **Detection Modes**
1. **All Enabled** - Uses all detectors enabled in configuration
2. **Only Selected** - Runs only checked detectors (overrides config)
3. **Exclude Selected** - Runs all except checked detectors (overrides config)

### **Output Formats**
1. **Detailed** - Complete report with line numbers, descriptions, and suggestions
2. **Summary** - Statistics by type and severity
3. **JSON** - Machine-readable format for integration

### **Configuration Precedence**
1. GUI detector selection (highest priority)
2. Configuration file settings
3. Default values (lowest priority)

## 📋 **How to Use**

### **Step 1: Select Files**
1. Click "📄 Select Java File" for single file analysis
2. Click "📁 Select Directory" for batch analysis
3. Selected files appear in the list below

### **Step 2: Configure Detection**
1. Choose detection mode (All/Only/Exclude)
2. Check/uncheck specific code smells
3. Select output format

### **Step 3: Run Analysis**
1. Click "🔍 Analyze Code"
2. Watch progress bar during analysis
3. Results automatically appear in Results tab

### **Step 4: Review Results**
1. Switch to Results tab to view findings
2. Save report using "💾 Save Report"
3. Copy results using "📋 Copy to Clipboard"

### **Step 5: Configure (Optional)**
1. Go to Configuration tab
2. Modify thresholds and settings
3. Save custom configurations
4. Apply changes with "✅ Apply Changes"

## 🔧 **Advanced Configuration**

The configuration file supports detailed customization:

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
    exclude_common: true
    exclude_constants: true

output:
  format: "detailed"
  include_line_numbers: true
  include_suggestions: true
```

## 🎨 **User Interface Features**

- **Tabbed Interface** - Organized into logical sections
- **Progress Tracking** - Visual feedback during analysis
- **Status Bar** - Real-time status updates
- **Tooltips** - Helpful descriptions on hover
- **Responsive Layout** - Adapts to window resizing
- **Keyboard Shortcuts** - Standard copy/paste support
- **Error Handling** - User-friendly error messages

## 🚀 **Performance Features**

- **Background Processing** - Analysis runs in separate thread
- **Non-blocking UI** - Interface remains responsive during analysis
- **Progress Indication** - Visual progress bar and status updates
- **Memory Efficient** - Processes files individually
- **Error Recovery** - Graceful handling of file access issues

## 📊 **Example Usage Workflow**

1. **Launch GUI**: `python launch_gui.py`
2. **Select Files**: Choose your Java project directory
3. **Configure**: Select "Only LongMethod,GodClass" for structural analysis
4. **Analyze**: Click analyze and wait for results
5. **Review**: Check detailed report in Results tab
6. **Export**: Save report for team review
7. **Adjust**: Modify thresholds in Configuration tab if needed
8. **Re-analyze**: Run again with updated settings

## 🎯 **Integration with Existing Workflow**

The GUI provides the same functionality as the CLI tool but with enhanced usability:

- **File Management** - Easy selection and organization
- **Visual Configuration** - No need to edit YAML files manually
- **Result Presentation** - Better formatted and searchable output
- **Batch Processing** - Analyze multiple files with one click
- **Export Options** - Save results in various formats

This GUI makes code smell detection accessible to developers who prefer graphical interfaces while maintaining all the power and flexibility of the command-line tool.