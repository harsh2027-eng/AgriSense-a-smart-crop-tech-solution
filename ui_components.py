# ui_components.py - UI Components and Widgets

import tkinter as tk
from tkinter import ttk
from config import (STYLES, COLORS, CROP_INPUT_FIELDS, FERTILIZER_DROPDOWN_FIELDS, 
                   FERTILIZER_NUMERIC_FIELDS, YIELD_DROPDOWN_FIELDS, YIELD_NUMERIC_FIELDS)

class UIComponents:
    def __init__(self, root):
        self.root = root
        self.setup_styles()
    
    def setup_styles(self):
        """Configure custom styles for the application"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure styles
        style.configure('Header.TLabel', **STYLES['header'], background=COLORS['background'])
        style.configure('SubHeader.TLabel', **STYLES['subheader'], background=COLORS['background'])
        style.configure('Info.TLabel', **STYLES['info'], background=COLORS['background'])
        style.configure('Custom.TNotebook', tabposition='n')
        style.configure('Custom.TNotebook.Tab', padding=[20, 10])
    
    def create_header(self, parent, title, subtitle):
        """Create application header"""
        header_frame = tk.Frame(parent, bg=COLORS['background'], pady=20)
        header_frame.pack(fill='x')
        
        title_label = ttk.Label(header_frame, text=title, style='Header.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text=subtitle, style='Info.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        return header_frame
    
    def create_input_panel(self, parent, title, input_fields, input_dict, field_type='entry'):
        """Create input panel with fields"""
        panel = tk.Frame(parent, bg=COLORS['white'], relief='raised', bd=2)
        panel.pack(side='left', fill='y', padx=(0, 10))
        
        ttk.Label(panel, text=title, style='SubHeader.TLabel').pack(pady=10)
        
        for label, key, *extra in input_fields:
            frame_input = tk.Frame(panel, bg=COLORS['white'])
            frame_input.pack(fill='x', padx=20, pady=5)
            
            ttk.Label(frame_input, text=label, background=COLORS['white']).pack(anchor='w')
            
            if field_type == 'entry':
                widget = tk.Entry(frame_input, font=STYLES['text']['font'], width=20)
                widget.pack(fill='x', pady=2)
            elif field_type == 'combobox':
                values = extra[0] if extra else []
                widget = ttk.Combobox(frame_input, values=values)
                widget.pack(fill='x', pady=2)
            
            input_dict[key] = widget
        
        return panel
    
    def create_result_panel(self, parent, title):
        """Create result display panel"""
        panel = tk.Frame(parent, bg=COLORS['white'], relief='raised', bd=2)
        panel.pack(side='right', fill='both', expand=True)
        
        ttk.Label(panel, text=title, style='SubHeader.TLabel').pack(pady=10)
        
        result_text = tk.Text(panel, height=15, wrap='word', 
                             font=STYLES['text']['font'], padx=10, pady=10)
        result_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        return panel, result_text
    
    def create_button_panel(self, parent, buttons):
        """Create panel with buttons"""
        button_frame = tk.Frame(parent, bg=COLORS['white'])
        button_frame.pack(pady=10)
        
        button_widgets = {}
        for text, command, key in buttons:
            btn = ttk.Button(button_frame, text=text, command=command)
            btn.pack(side='left', padx=5)
            if key:
                button_widgets[key] = btn
        
        return button_frame, button_widgets
    
    def create_data_tree(self, parent, columns, height=10):
        """Create treeview for data display"""
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=height)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        return tree, scrollbar
    
    def create_status_bar(self, parent):
        """Create status bar"""
        status_frame = tk.Frame(parent, relief='sunken', bd=1, bg=COLORS['light_gray'])
        status_frame.pack(side='bottom', fill='x')
        
        status_label = tk.Label(status_frame, text="Ready", 
                               bg=COLORS['light_gray'], font=STYLES['status']['font'])
        status_label.pack(side='left', padx=10, pady=2)
        
        time_label = tk.Label(status_frame, text="", 
                             bg=COLORS['light_gray'], font=STYLES['status']['font'])
        time_label.pack(side='right', padx=10, pady=2)
        
        return status_frame, status_label, time_label
    
    def create_notebook(self, parent):
        """Create main notebook widget"""
        notebook = ttk.Notebook(parent, style='Custom.TNotebook')
        notebook.pack(fill='both', expand=True)
        return notebook
    
    def create_tab_content(self, notebook, tab_name, icon=""):
        """Create tab and return its frame"""
        frame = ttk.Frame(notebook)
        display_name = f"{icon} {tab_name}" if icon else tab_name
        notebook.add(frame, text=display_name)
        return frame
    
    def create_main_container(self, parent):
        """Create main container for tab content"""
        container = tk.Frame(parent, bg=COLORS['white'])
        container.pack(fill='both', expand=True, padx=10, pady=10)
        return container
    
    def create_chart_frame(self, parent):
        """Create frame for charts"""
        chart_frame = tk.Frame(parent, bg=COLORS['white'], relief='raised', bd=2)
        chart_frame.pack(fill='both', expand=True, padx=10, pady=5)
        return chart_frame
    
    def update_result_text(self, text_widget, content):
        """Update text widget content"""
        text_widget.delete(1.0, tk.END)
        text_widget.insert(1.0, content)
    
    def clear_inputs(self, input_dict):
        """Clear all input fields"""
        for widget in input_dict.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
    
    def get_input_values(self, input_dict, required_fields=None):
        """Get values from input widgets"""
        values = {}
        missing_fields = []
        
        for key, widget in input_dict.items():
            if isinstance(widget, (tk.Entry, ttk.Combobox)):
                value = widget.get().strip()
                values[key] = value
                
                if required_fields and key in required_fields and not value:
                    missing_fields.append(key)
        
        return values, missing_fields
    
    def validate_numeric_inputs(self, input_dict, numeric_fields):
        """Validate numeric input fields"""
        validated_values = {}
        errors = []
        
        for key in numeric_fields:
            if key in input_dict:
                try:
                    value = float(input_dict[key])
                    validated_values[key] = value
                except ValueError:
                    errors.append(f"Invalid numeric value for {key}")
        
        return validated_values, errors
    
    def set_widget_state(self, widget, state='normal'):
        """Set widget state (normal, disabled)"""
        try:
            widget.configure(state=state)
        except:
            pass  # Some widgets might not support state changes
    
    def create_progress_bar(self, parent):
        """Create progress bar widget"""
        progress = ttk.Progressbar(parent, mode='indeterminate')
        return progress
    
    def create_separator(self, parent, orient='horizontal'):
        """Create separator widget"""
        separator = ttk.Separator(parent, orient=orient)
        return separator