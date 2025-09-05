# main_gui.py - Main GUI Application

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from config import APP_CONFIG, CROP_INPUT_FIELDS, FERTILIZER_DROPDOWN_FIELDS, FERTILIZER_NUMERIC_FIELDS
from config import YIELD_DROPDOWN_FIELDS, YIELD_NUMERIC_FIELDS, STATE_DISTRICT_MAPPING
from data_generator import DataGenerator
from ml_models import CropMLModels
from prediction_engine import PredictionEngine
from visualizations import CropVisualizations
from data_manager import DataManager
from ui_components import UIComponents

class CropManagementSystem:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Initialize components
        self.ui = UIComponents(root)
        self.data_generator = DataGenerator()
        self.ml_models = CropMLModels()
        self.data_manager = DataManager()
        self.prediction_engine = PredictionEngine(self.ml_models)
        
        # Initialize variables
        self.crop_inputs = {}
        self.fertilizer_inputs = {}
        self.yield_inputs = {}
        
        # Create UI
        self.create_interface()
        
        # Initialize data and train models
        self.initialize_system()
    
    def setup_window(self):
        """Setup main window properties"""
        self.root.title(APP_CONFIG['title'])
        self.root.geometry(APP_CONFIG['geometry'])
        self.root.configure(bg=APP_CONFIG['background'])
        self.root.minsize(APP_CONFIG['min_width'], APP_CONFIG['min_height'])
    
    def create_interface(self):
        """Create the main interface"""
        # Create header
        self.ui.create_header(
            self.root, 
            APP_CONFIG['title'],
            "AI-Powered Agricultural Decision Support System"
        )
        
        # Create main frame and notebook
        main_frame = tk.Frame(self.root, bg=APP_CONFIG['background'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.notebook = self.ui.create_notebook(main_frame)
        
        # Create tabs
        self.create_crop_recommendation_tab()
        self.create_fertilizer_tab()
        self.create_yield_prediction_tab()
        self.create_analysis_tab()
        self.create_data_management_tab()
        
        # Create status bar
        self.status_frame, self.status_label, self.time_label = self.ui.create_status_bar(self.root)
    
    def on_state_selected(self, event=None):
        """Handle state selection and update district dropdown"""
        selected_state = self.yield_inputs['state'].get()
        if selected_state in STATE_DISTRICT_MAPPING:
            districts = STATE_DISTRICT_MAPPING[selected_state]
            self.yield_inputs['district']['values'] = districts
            self.yield_inputs['district'].set('')  # Clear current selection
    
    def create_crop_recommendation_tab(self):
        """Create crop recommendation tab"""
        tab_frame = self.ui.create_tab_content(self.notebook, "Crop Recommendation", "🌱")
        main_container = self.ui.create_main_container(tab_frame)
        
        # Create input panel
        left_panel = self.ui.create_input_panel(
            main_container,
            "Soil & Weather Parameters",
            CROP_INPUT_FIELDS,
            self.crop_inputs,
            'entry'
        )
        
        # Add predict button to left panel
        predict_btn = tk.Button(left_panel, text="🔍 Get Crop Recommendation", 
                               command=self.predict_crop, 
                               bg='#3498db', fg='white', font=('Arial', 10, 'bold'))
        predict_btn.pack(pady=20)
        
        # Create result panel
        right_panel, self.crop_result = self.ui.create_result_panel(
            main_container,
            "Recommendation Results"
        )
    
    def create_fertilizer_tab(self):
        """Create fertilizer recommendation tab"""
        tab_frame = self.ui.create_tab_content(self.notebook, "Fertilizer Recommendation", "🧪")
        main_container = self.ui.create_main_container(tab_frame)
        
        # Left panel for inputs
        left_panel = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        tk.Label(left_panel, text="Crop & Soil Information", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Create dropdown fields
        for label, key, values in FERTILIZER_DROPDOWN_FIELDS:
            frame_input = tk.Frame(left_panel, bg='white')
            frame_input.pack(fill='x', padx=20, pady=5)
            
            tk.Label(frame_input, text=label, bg='white').pack(anchor='w')
            combo = tk.ttk.Combobox(frame_input, values=values)
            combo.pack(fill='x', pady=2)
            self.fertilizer_inputs[key] = combo
        
        # Create numeric fields
        for label, key in FERTILIZER_NUMERIC_FIELDS:
            frame_input = tk.Frame(left_panel, bg='white')
            frame_input.pack(fill='x', padx=20, pady=5)
            
            tk.Label(frame_input, text=label, bg='white').pack(anchor='w')
            entry = tk.Entry(frame_input, font=('Arial', 10), width=20)
            entry.pack(fill='x', pady=2)
            self.fertilizer_inputs[key] = entry
        
        # Add predict button
        predict_btn = tk.Button(left_panel, text="🧪 Get Fertilizer Recommendation", 
                               command=self.predict_fertilizer,
                               bg='#e74c3c', fg='white', font=('Arial', 10, 'bold'))
        predict_btn.pack(pady=20)
        
        # Create result panel
        right_panel, self.fertilizer_result = self.ui.create_result_panel(
            main_container,
            "Fertilizer Recommendation"
        )
    
    def create_yield_prediction_tab(self):
        """Create yield prediction tab"""
        tab_frame = self.ui.create_tab_content(self.notebook, "Yield Prediction", "📊")
        main_container = self.ui.create_main_container(tab_frame)
        
        # Left panel for inputs
        left_panel = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        
        tk.Label(left_panel, text="Crop Information", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Create dropdown fields with dynamic district selection
        for label, key, values in YIELD_DROPDOWN_FIELDS:
            frame_input = tk.Frame(left_panel, bg='white')
            frame_input.pack(fill='x', padx=20, pady=5)
            
            tk.Label(frame_input, text=label, bg='white').pack(anchor='w')
            combo = tk.ttk.Combobox(frame_input, values=values)
            combo.pack(fill='x', pady=2)
            self.yield_inputs[key] = combo
            
            # Bind state selection to update districts
            if key == 'state':
                combo.bind('<<ComboboxSelected>>', self.on_state_selected)
        
        # Create numeric fields
        for label, key in YIELD_NUMERIC_FIELDS:
            frame_input = tk.Frame(left_panel, bg='white')
            frame_input.pack(fill='x', padx=20, pady=5)
            
            tk.Label(frame_input, text=label, bg='white').pack(anchor='w')
            entry = tk.Entry(frame_input, font=('Arial', 10), width=20)
            entry.pack(fill='x', pady=2)
            self.yield_inputs[key] = entry
        
        # Add predict button
        predict_btn = tk.Button(left_panel, text="📊 Predict Yield", 
                               command=self.predict_yield,
                               bg='#27ae60', fg='white', font=('Arial', 10, 'bold'))
        predict_btn.pack(pady=20)
        
        # Create result panel
        right_panel, self.yield_result = self.ui.create_result_panel(
            main_container,
            "Yield Prediction Results"
        )
    
    def create_analysis_tab(self):
        """Create data analysis and visualization tab"""
        tab_frame = self.ui.create_tab_content(self.notebook, "Data Analysis", "📈")
        main_container = self.ui.create_main_container(tab_frame)
        
        # Control panel
        control_panel = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        control_panel.pack(fill='x', padx=10, pady=5)
        
        tk.Label(control_panel, text="Analysis Options", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=5)
        
        # Create buttons
        buttons = [
            ("📊 Crop Distribution", self.show_crop_distribution, None),
            ("🌡️ Parameter Analysis", self.show_parameter_analysis, None),
            ("📈 Yield Trends", self.show_yield_trends, None)
        ]
        
        self.ui.create_button_panel(control_panel, buttons)
        
        # Chart area
        self.chart_frame = self.ui.create_chart_frame(main_container)
        self.visualizations = CropVisualizations(self.chart_frame)
    
    def create_data_management_tab(self):
        """Create data management tab"""
        tab_frame = self.ui.create_tab_content(self.notebook, "Data Management", "💾")
        main_container = self.ui.create_main_container(tab_frame)
        
        # Control panel
        control_panel = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        control_panel.pack(fill='x', padx=10, pady=5)
        
        tk.Label(control_panel, text="Data Operations", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # Create buttons
        buttons = [
            ("📁 Load Data", self.load_data, None),
            ("💾 Export Results", self.export_data, None),
            ("🔄 Retrain Models", self.retrain_models, None)
        ]
        
        self.ui.create_button_panel(control_panel, buttons)
        
        # Data preview
        data_frame = tk.Frame(main_container, bg='white', relief='raised', bd=2)
        data_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        tk.Label(data_frame, text="Data Preview", 
                font=('Arial', 14, 'bold'), bg='white').pack(pady=5)
        
        # Create treeview for data display
        columns = ['Dataset', 'Samples', 'Features', 'Status']
        self.data_tree, scrollbar = self.ui.create_data_tree(data_frame, columns, height=10)
        
        # Pack treeview and scrollbar
        self.data_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
    
    def initialize_system(self):
        """Initialize system with data and trained models"""
        self.update_status("Initializing system...")
        
        try:
            # Generate sample data
            data = self.data_generator.generate_all_data()
            self.data_manager.set_data(data)
            
            # Train models
            self.train_models()
            
            # Update data tree
            self.update_data_tree()
            
            self.update_status("System initialized successfully!")
            
        except Exception as e:
            error_msg = f"System initialization failed: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Initialization Error", error_msg)
    
    def train_models(self):
        """Train all machine learning models"""
        self.update_status("Training models...")
        
        try:
            data = self.data_manager.data
            results = self.ml_models.train_all_models(data)
            
            # Log training results
            training_info = "Model Training Results:\n"
            for model_name, result in results.items():
                if 'test_accuracy' in result:
                    training_info += f"{model_name}: {result['test_accuracy']:.3f} accuracy\n"
                elif 'test_score' in result:
                    training_info += f"{model_name}: {result['test_score']:.3f} R² score\n"
            
            print(training_info)  # Log to console
            self.update_status("Models trained successfully!")
            
        except Exception as e:
            error_msg = f"Model training failed: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Training Error", error_msg)
    
    def predict_crop(self):
        """Handle crop prediction"""
        try:
            # Get input values
            values, missing = self.ui.get_input_values(self.crop_inputs, CROP_INPUT_FIELDS)
            
            if missing:
                messagebox.showerror("Error", f"Please fill in: {', '.join([field[0] for field in CROP_INPUT_FIELDS if field[1] in missing])}")
                return
            
            # Validate numeric inputs
            numeric_values, errors = self.ui.validate_numeric_inputs(values, [field[1] for field in CROP_INPUT_FIELDS])
            
            if errors:
                messagebox.showerror("Error", "\n".join(errors))
                return
            
            # Prepare inputs for prediction
            inputs = [numeric_values[field[1]] for field in CROP_INPUT_FIELDS]
            
            # Make prediction
            result = self.prediction_engine.predict_crop(inputs)
            
            if result['success']:
                self.ui.update_result_text(self.crop_result, result['results'])
                self.update_status(f"Crop prediction completed: {result['prediction']}")
            else:
                messagebox.showerror("Prediction Error", result['error'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")
    
    def predict_fertilizer(self):
        """Handle fertilizer prediction"""
        try:
            # Get input values
            values, missing = self.ui.get_input_values(self.fertilizer_inputs)
            
            if missing:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            # Separate categorical and numeric inputs
            categorical_inputs = {
                'soil_type': values['soil_type'],
                'crop_type': values['crop_type']
            }
            
            numeric_fields = [field[1] for field in FERTILIZER_NUMERIC_FIELDS]
            numeric_inputs, errors = self.ui.validate_numeric_inputs(values, numeric_fields)
            
            if errors:
                messagebox.showerror("Error", "\n".join(errors))
                return
            
            # Make prediction
            result = self.prediction_engine.predict_fertilizer(categorical_inputs, numeric_inputs)
            
            if result['success']:
                self.ui.update_result_text(self.fertilizer_result, result['results'])
                self.update_status(f"Fertilizer recommendation completed: {result['prediction']}")
            else:
                messagebox.showerror("Prediction Error", result['error'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")
    
    def predict_yield(self):
        """Handle yield prediction"""
        try:
            # Get input values
            values, missing = self.ui.get_input_values(self.yield_inputs)
            
            if missing:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            # Separate categorical and numeric inputs
            categorical_inputs = {
                'state': values['state'],
                'district': values['district'],
                'season': values['season'],
                'crop': values['crop']
            }
            
            numeric_fields = [field[1] for field in YIELD_NUMERIC_FIELDS]
            numeric_inputs, errors = self.ui.validate_numeric_inputs(values, numeric_fields)
            
            if errors:
                messagebox.showerror("Error", "\n".join(errors))
                return
            
            # Make prediction
            result = self.prediction_engine.predict_yield(categorical_inputs, numeric_inputs)
            
            if result['success']:
                self.ui.update_result_text(self.yield_result, result['results'])
                self.update_status(f"Yield prediction completed: {result['prediction']:.2f} tons/hectare")
            else:
                messagebox.showerror("Prediction Error", result['error'])
                
        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")
    
    def show_crop_distribution(self):
        """Show crop distribution visualization"""
        try:
            self.visualizations.show_crop_distribution(self.data_manager.data)
            self.update_status("Crop distribution chart generated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate chart: {str(e)}")
    
    def show_parameter_analysis(self):
        """Show parameter analysis visualization"""
        try:
            self.visualizations.show_parameter_analysis(self.data_manager.data)
            self.update_status("Parameter analysis chart generated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate chart: {str(e)}")
    
    def show_yield_trends(self):
        """Show yield trends visualization"""
        try:
            self.visualizations.show_yield_trends(self.data_manager.data)
            self.update_status("Yield trends chart generated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate chart: {str(e)}")
    
    def load_data(self):
        """Load data from file"""
        success, message = self.data_manager.load_csv_data(self.root)
        if success:
            self.update_data_tree()
            # Optionally retrain models with new data
            response = messagebox.askyesno("Retrain Models", 
                                          "Data loaded successfully. Do you want to retrain models with new data?")
            if response:
                self.train_models()
        
        self.update_status(message)
    
    def export_data(self):
        """Export data to file"""
        success, message = self.data_manager.export_data(parent_window=self.root)
        self.update_status(message)
    
    def retrain_models(self):
        """Retrain all models"""
        response = messagebox.askyesno("Retrain Models", 
                                      "This will retrain all models with current data. Continue?")
        if response:
            self.train_models()
            self.update_data_tree()
            messagebox.showinfo("Success", "All models have been retrained successfully!")
    
    def update_data_tree(self):
        """Update the data tree view"""
        # Clear existing items
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        # Add current data information
        data_info = self.data_manager.get_dataset_info()
        for info in data_info:
            self.data_tree.insert('', 'end', values=info)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.time_label.config(text=f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.root.update_idletasks()

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = CropManagementSystem(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()