#!/usr/bin/env python3
"""
Code Smell Detector GUI
A user-friendly graphical interface for detecting code smells in Java files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
import yaml
import json
from detector_engine import CodeSmellDetector

class CodeSmellDetectorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Smell Detector - Java Code Analysis Tool")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)
        
        # Initialize detector
        self.detector = None
        self.config_path = None
        self.selected_files = []
        
        # Configure style
        self.setup_styles()
        
        # Create GUI components
        self.create_widgets()
        
        # Initialize detector
        self.initialize_detector()
        
    def setup_styles(self):
        """Setup custom styles for the GUI"""
        style = ttk.Style()
        
        # Configure notebook style
        style.configure('Custom.TNotebook', tabposition='n')
        style.configure('Custom.TNotebook.Tab', padding=[20, 10])
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        style.configure('Danger.TButton', foreground='red')
        style.configure('Success.TButton', foreground='green')
        
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🔍 Code Smell Detector", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.create_analysis_tab()
        self.create_configuration_tab()
        self.create_results_tab()
        self.create_help_tab()
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_analysis_tab(self):
        """Create the main analysis tab"""
        analysis_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(analysis_frame, text="📁 File Analysis")
        
        analysis_frame.columnconfigure(1, weight=1)
        
        # File selection section
        file_section = ttk.LabelFrame(analysis_frame, text="📂 File Selection", padding="15")
        file_section.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        file_section.columnconfigure(1, weight=1)
        
        # File selection buttons
        ttk.Button(file_section, text="📄 Select Java File", 
                  command=self.select_file, style='Action.TButton').grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(file_section, text="📁 Select Directory", 
                  command=self.select_directory, style='Action.TButton').grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(file_section, text="🗑️ Clear Selection", 
                  command=self.clear_selection, style='Danger.TButton').grid(row=0, column=2)
        
        # Selected files display
        ttk.Label(file_section, text="Selected Files:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        
        self.files_listbox = tk.Listbox(file_section, height=4, selectmode=tk.EXTENDED)
        self.files_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scrollbar for listbox
        files_scrollbar = ttk.Scrollbar(file_section, orient=tk.VERTICAL, command=self.files_listbox.yview)
        files_scrollbar.grid(row=2, column=3, sticky=(tk.N, tk.S))
        self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
        
        # Detection settings section
        settings_section = ttk.LabelFrame(analysis_frame, text="⚙️ Detection Settings", padding="15")
        settings_section.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        settings_section.columnconfigure(1, weight=1)
        
        # Detection mode
        ttk.Label(settings_section, text="Detection Mode:").grid(row=0, column=0, sticky=tk.W)
        
        self.detection_mode = tk.StringVar(value="all")
        mode_frame = ttk.Frame(settings_section)
        mode_frame.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Radiobutton(mode_frame, text="All Enabled", variable=self.detection_mode, 
                       value="all").grid(row=0, column=0, padx=(0, 15))
        ttk.Radiobutton(mode_frame, text="Only Selected", variable=self.detection_mode, 
                       value="only").grid(row=0, column=1, padx=(0, 15))
        ttk.Radiobutton(mode_frame, text="Exclude Selected", variable=self.detection_mode, 
                       value="exclude").grid(row=0, column=2)
        
        # Code smell selection
        self.create_smell_selection(settings_section)
        
        # Output format
        ttk.Label(settings_section, text="Output Format:").grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        
        self.output_format = tk.StringVar(value="detailed")
        format_frame = ttk.Frame(settings_section)
        format_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        ttk.Radiobutton(format_frame, text="Detailed", variable=self.output_format, 
                       value="detailed").grid(row=0, column=0, padx=(0, 15))
        ttk.Radiobutton(format_frame, text="Summary", variable=self.output_format, 
                       value="summary").grid(row=0, column=1, padx=(0, 15))
        ttk.Radiobutton(format_frame, text="JSON", variable=self.output_format, 
                       value="json").grid(row=0, column=2)
        
        # Analysis controls
        controls_frame = ttk.Frame(analysis_frame)
        controls_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15))
        
        self.analyze_button = ttk.Button(controls_frame, text="🔍 Analyze Code", 
                                        command=self.start_analysis, style='Action.TButton')
        self.analyze_button.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(controls_frame, text="💾 Save Report", 
                  command=self.save_report).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(controls_frame, text="📋 Copy to Clipboard", 
                  command=self.copy_to_clipboard).grid(row=0, column=2)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(analysis_frame, variable=self.progress_var, 
                                           mode='indeterminate')
        self.progress_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
    def create_smell_selection(self, parent):
        """Create code smell selection checkboxes"""
        ttk.Label(parent, text="Code Smells:").grid(row=1, column=0, sticky=(tk.W, tk.N), pady=(10, 0))
        
        smells_frame = ttk.Frame(parent)
        smells_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        self.smell_vars = {}
        smell_descriptions = {
            'LongMethod': 'Long Method - Methods that are too long',
            'GodClass': 'God Class - Classes with too many responsibilities',
            'DuplicatedCode': 'Duplicated Code - Repeated code blocks',
            'LargeParameterList': 'Large Parameter List - Too many parameters',
            'MagicNumbers': 'Magic Numbers - Hardcoded numeric values',
            'FeatureEnvy': 'Feature Envy - Methods interested in other classes'
        }
        
        row = 0
        col = 0
        for smell, description in smell_descriptions.items():
            var = tk.BooleanVar(value=True)
            self.smell_vars[smell] = var
            
            cb = ttk.Checkbutton(smells_frame, text=smell, variable=var)
            cb.grid(row=row, column=col, sticky=tk.W, padx=(0, 20), pady=2)
            
            # Tooltip (simple implementation)
            self.create_tooltip(cb, description)
            
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
        
        # Select/Deselect all buttons
        button_frame = ttk.Frame(smells_frame)
        button_frame.grid(row=row+1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Select All", 
                  command=self.select_all_smells).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Deselect All", 
                  command=self.deselect_all_smells).grid(row=0, column=1)
        
    def create_tooltip(self, widget, text):
        """Create a simple tooltip for a widget"""
        def on_enter(event):
            self.update_status(text)
        
        def on_leave(event):
            self.update_status("Ready")
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
        
    def create_configuration_tab(self):
        """Create the configuration tab"""
        config_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(config_frame, text="⚙️ Configuration")
        
        config_frame.columnconfigure(0, weight=1)
        config_frame.rowconfigure(1, weight=1)
        
        # Configuration info
        info_label = ttk.Label(config_frame, 
                              text="Configure detection thresholds and settings for each code smell type.",
                              font=('Arial', 10))
        info_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        # Configuration editor
        config_editor_frame = ttk.LabelFrame(config_frame, text="Configuration Editor", padding="15")
        config_editor_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        config_editor_frame.columnconfigure(0, weight=1)
        config_editor_frame.rowconfigure(0, weight=1)
        
        self.config_text = scrolledtext.ScrolledText(config_editor_frame, wrap=tk.WORD, 
                                                    height=20, font=('Consolas', 10))
        self.config_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuration controls
        config_controls = ttk.Frame(config_frame)
        config_controls.grid(row=2, column=0, pady=(15, 0))
        
        ttk.Button(config_controls, text="📁 Load Config", 
                  command=self.load_config_file).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(config_controls, text="💾 Save Config", 
                  command=self.save_config_file).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(config_controls, text="🔄 Reset to Default", 
                  command=self.reset_config).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(config_controls, text="✅ Apply Changes", 
                  command=self.apply_config_changes, style='Success.TButton').grid(row=0, column=3)
        
    def create_results_tab(self):
        """Create the results display tab"""
        results_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(results_frame, text="📊 Results")
        
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Results header
        header_frame = ttk.Frame(results_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        header_frame.columnconfigure(1, weight=1)
        
        ttk.Label(header_frame, text="Analysis Results", 
                 font=('Arial', 14, 'bold')).grid(row=0, column=0, sticky=tk.W)
        
        self.results_info_label = ttk.Label(header_frame, text="No analysis performed yet")
        self.results_info_label.grid(row=0, column=1, sticky=tk.E)
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 10))
        self.results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results controls
        results_controls = ttk.Frame(results_frame)
        results_controls.grid(row=2, column=0, pady=(15, 0))
        
        ttk.Button(results_controls, text="🗑️ Clear Results", 
                  command=self.clear_results).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(results_controls, text="💾 Export Results", 
                  command=self.export_results).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(results_controls, text="📋 Copy Results", 
                  command=self.copy_results).grid(row=0, column=2)
        
    def create_help_tab(self):
        """Create the help and about tab"""
        help_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(help_frame, text="❓ Help")
        
        help_frame.columnconfigure(0, weight=1)
        help_frame.rowconfigure(0, weight=1)
        
        help_text = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD, font=('Arial', 10))
        help_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        help_content = """
🔍 CODE SMELL DETECTOR HELP

OVERVIEW
--------
This tool detects common code smells in Java source files to help improve code quality and maintainability.

SUPPORTED CODE SMELLS
--------------------
• Long Method - Methods that are excessively long and do too much
• God Class (Blob) - Classes with too many responsibilities  
• Duplicated Code - Similar code blocks that should be refactored
• Large Parameter List - Methods with too many parameters
• Magic Numbers - Hardcoded numeric values that should be constants
• Feature Envy - Methods overly interested in other classes' data

HOW TO USE
----------
1. FILE SELECTION:
   - Click "Select Java File" to analyze a single .java file
   - Click "Select Directory" to analyze all .java files in a folder
   - Selected files will appear in the list below

2. DETECTION SETTINGS:
   - Choose detection mode:
     * All Enabled: Use all detectors enabled in configuration
     * Only Selected: Run only the checked detectors
     * Exclude Selected: Run all except the checked detectors
   - Select/deselect specific code smells to analyze
   - Choose output format (Detailed, Summary, or JSON)

3. ANALYSIS:
   - Click "Analyze Code" to start detection
   - Progress will be shown in the progress bar
   - Results will appear in the Results tab

4. CONFIGURATION:
   - Use the Configuration tab to adjust detection thresholds
   - Modify YAML configuration directly in the editor
   - Load/save custom configuration files
   - Apply changes to update the detector

OUTPUT FORMATS
--------------
• Detailed: Complete report with line numbers, descriptions, and suggestions
• Summary: Statistics by smell type and severity
• JSON: Machine-readable format for integration with other tools

CONFIGURATION OPTIONS
--------------------
The detector can be customized through the config.yaml file:

• Thresholds: Adjust sensitivity for each code smell type
• Enabled/Disabled: Turn specific detectors on/off
• Output Settings: Configure report formatting
• File Patterns: Set which files to include/exclude

TIPS FOR BEST RESULTS
--------------------
• Analyze smaller codebases first to understand the tool
• Review detailed reports to learn about specific issues
• Adjust thresholds in configuration for your coding standards
• Use the exclude mode to focus on specific smell types
• Export results for documentation and team reviews

ABOUT
-----
Code Smell Detector v1.0
Created for educational purposes to demonstrate code quality analysis.
Supports Java source code analysis with six major code smell patterns.

For more information about code smells and refactoring techniques,
refer to "Refactoring: Improving the Design of Existing Code" by Martin Fowler.
        """
        
        help_text.insert(tk.END, help_content)
        help_text.configure(state=tk.DISABLED)
        
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Detector info
        self.detector_info_label = ttk.Label(status_frame, text="Detector: Not loaded")
        self.detector_info_label.grid(row=0, column=2, sticky=tk.E)
        
    def initialize_detector(self):
        """Initialize the code smell detector"""
        try:
            self.detector = CodeSmellDetector()
            self.load_current_config()
            self.update_status("Detector initialized successfully")
            self.detector_info_label.config(text=f"Detector: Ready ({len(self.detector.get_available_detectors())} detectors)")
        except Exception as e:
            self.update_status(f"Error initializing detector: {str(e)}")
            messagebox.showerror("Initialization Error", f"Failed to initialize detector:\n{str(e)}")
            
    def load_current_config(self):
        """Load current configuration into the editor"""
        try:
            if self.detector and self.detector.config:
                config_yaml = yaml.dump(self.detector.config, default_flow_style=False, sort_keys=False)
                self.config_text.delete(1.0, tk.END)
                self.config_text.insert(1.0, config_yaml)
        except Exception as e:
            self.update_status(f"Error loading config: {str(e)}")
            
    def select_file(self):
        """Select a single Java file"""
        filename = filedialog.askopenfilename(
            title="Select Java File",
            filetypes=[("Java files", "*.java"), ("All files", "*.*")]
        )
        if filename:
            self.selected_files = [filename]
            self.update_file_list()
            self.update_status(f"Selected file: {os.path.basename(filename)}")
            
    def select_directory(self):
        """Select a directory containing Java files"""
        directory = filedialog.askdirectory(title="Select Directory")
        if directory:
            java_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.java'):
                        java_files.append(os.path.join(root, file))
            
            if java_files:
                self.selected_files = java_files
                self.update_file_list()
                self.update_status(f"Selected {len(java_files)} Java files from directory")
            else:
                messagebox.showwarning("No Java Files", "No Java files found in the selected directory.")
                
    def clear_selection(self):
        """Clear file selection"""
        self.selected_files = []
        self.update_file_list()
        self.update_status("File selection cleared")
        
    def update_file_list(self):
        """Update the file list display"""
        self.files_listbox.delete(0, tk.END)
        for file_path in self.selected_files:
            display_name = os.path.basename(file_path)
            self.files_listbox.insert(tk.END, display_name)
            
    def select_all_smells(self):
        """Select all code smell checkboxes"""
        for var in self.smell_vars.values():
            var.set(True)
            
    def deselect_all_smells(self):
        """Deselect all code smell checkboxes"""
        for var in self.smell_vars.values():
            var.set(False)
            
    def start_analysis(self):
        """Start code analysis in a separate thread"""
        if not self.selected_files:
            messagebox.showwarning("No Files Selected", "Please select Java files to analyze.")
            return
            
        if not self.detector:
            messagebox.showerror("Detector Error", "Detector not initialized.")
            return
            
        # Disable analyze button and start progress
        self.analyze_button.config(state=tk.DISABLED)
        self.progress_bar.start()
        self.update_status("Analyzing code...")
        
        # Start analysis in background thread
        thread = threading.Thread(target=self.run_analysis)
        thread.daemon = True
        thread.start()
        
    def run_analysis(self):
        """Run the actual analysis (called in background thread)"""
        try:
            # Configure detector based on GUI settings
            self.configure_detector()
            
            # Analyze files
            all_smells = []
            for file_path in self.selected_files:
                smells = self.detector.analyze_file(file_path)
                all_smells.extend(smells)
            
            # Generate report
            report = self.detector.generate_report(all_smells)
            
            # Update GUI in main thread
            self.root.after(0, self.analysis_complete, report, len(all_smells))
            
        except Exception as e:
            self.root.after(0, self.analysis_error, str(e))
            
    def configure_detector(self):
        """Configure detector based on GUI settings"""
        mode = self.detection_mode.get()
        selected_smells = [smell for smell, var in self.smell_vars.items() if var.get()]
        
        if mode == "only":
            self.detector.configure_active_detectors(only=selected_smells)
        elif mode == "exclude":
            self.detector.configure_active_detectors(exclude=selected_smells)
        else:  # "all"
            self.detector.configure_active_detectors()
            
        # Set output format
        self.detector.config['output']['format'] = self.output_format.get()
        
    def analysis_complete(self, report, smell_count):
        """Handle analysis completion (called in main thread)"""
        self.progress_bar.stop()
        self.analyze_button.config(state=tk.NORMAL)
        
        # Update results
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, report)
        
        # Update info
        file_count = len(self.selected_files)
        active_detectors = ", ".join(self.detector.active_detectors)
        self.results_info_label.config(
            text=f"Files: {file_count} | Smells: {smell_count} | Detectors: {active_detectors}"
        )
        
        # Switch to results tab
        self.notebook.select(2)  # Results tab
        
        self.update_status(f"Analysis complete: {smell_count} smells found in {file_count} files")
        
    def analysis_error(self, error_message):
        """Handle analysis error (called in main thread)"""
        self.progress_bar.stop()
        self.analyze_button.config(state=tk.NORMAL)
        self.update_status(f"Analysis failed: {error_message}")
        messagebox.showerror("Analysis Error", f"Analysis failed:\n{error_message}")
        
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def save_report(self):
        """Save current analysis report"""
        if not hasattr(self, 'results_text') or not self.results_text.get(1.0, tk.END).strip():
            messagebox.showwarning("No Results", "No analysis results to save.")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Report",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.results_text.get(1.0, tk.END))
                self.update_status(f"Report saved: {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Report saved successfully!")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save report:\n{str(e)}")
                
    def copy_to_clipboard(self):
        """Copy results to clipboard"""
        if not hasattr(self, 'results_text') or not self.results_text.get(1.0, tk.END).strip():
            messagebox.showwarning("No Results", "No analysis results to copy.")
            return
            
        self.root.clipboard_clear()
        self.root.clipboard_append(self.results_text.get(1.0, tk.END))
        self.update_status("Results copied to clipboard")
        
    def load_config_file(self):
        """Load configuration from file"""
        filename = filedialog.askopenfilename(
            title="Load Configuration",
            filetypes=[("YAML files", "*.yaml"), ("YAML files", "*.yml"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    config_content = f.read()
                self.config_text.delete(1.0, tk.END)
                self.config_text.insert(1.0, config_content)
                self.update_status(f"Configuration loaded: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load configuration:\n{str(e)}")
                
    def save_config_file(self):
        """Save configuration to file"""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration",
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("YAML files", "*.yml"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.config_text.get(1.0, tk.END))
                self.update_status(f"Configuration saved: {os.path.basename(filename)}")
                messagebox.showinfo("Success", "Configuration saved successfully!")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save configuration:\n{str(e)}")
                
    def reset_config(self):
        """Reset configuration to default"""
        if messagebox.askyesno("Reset Configuration", "Reset configuration to default values?"):
            try:
                self.detector = CodeSmellDetector()  # Reload with default config
                self.load_current_config()
                self.update_status("Configuration reset to default")
            except Exception as e:
                messagebox.showerror("Reset Error", f"Failed to reset configuration:\n{str(e)}")
                
    def apply_config_changes(self):
        """Apply configuration changes"""
        try:
            config_text = self.config_text.get(1.0, tk.END)
            new_config = yaml.safe_load(config_text)
            
            # Validate configuration
            if not isinstance(new_config, dict):
                raise ValueError("Configuration must be a valid YAML dictionary")
                
            # Apply new configuration
            self.detector.config = new_config
            self.detector._initialize_detectors()
            
            self.update_status("Configuration applied successfully")
            messagebox.showinfo("Success", "Configuration changes applied successfully!")
            
        except yaml.YAMLError as e:
            messagebox.showerror("YAML Error", f"Invalid YAML configuration:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Failed to apply configuration:\n{str(e)}")
            
    def clear_results(self):
        """Clear analysis results"""
        self.results_text.delete(1.0, tk.END)
        self.results_info_label.config(text="No analysis performed yet")
        self.update_status("Results cleared")
        
    def export_results(self):
        """Export results in different formats"""
        self.save_report()  # Reuse save functionality
        
    def copy_results(self):
        """Copy results to clipboard"""
        self.copy_to_clipboard()  # Reuse copy functionality


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = CodeSmellDetectorGUI(root)
    
    # Set icon (if available)
    try:
        # You can add an icon file here
        # root.iconbitmap('icon.ico')
        pass
    except:
        pass
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()