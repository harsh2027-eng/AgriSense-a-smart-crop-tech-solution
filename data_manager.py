# data_manager.py - Data Management and File Operations

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os

class DataManager:
    def __init__(self):
        self.data = {}
        self.data_info = {}
    
    def set_data(self, data_dict):
        """Set the data dictionary"""
        self.data = data_dict
        self.update_data_info()
    
    def update_data_info(self):
        """Update data information"""
        self.data_info = {}
        for name, df in self.data.items():
            self.data_info[name] = {
                'samples': len(df),
                'features': len(df.columns),
                'status': 'Ready',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M')
            }
    
    def load_csv_data(self, parent_window=None):
        """Load data from CSV file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select CSV file",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                parent=parent_window
            )
            
            if file_path:
                # Load the data
                new_data = pd.read_csv(file_path)
                
                # Show data info dialog
                info_text = f"Data loaded successfully!\n\n"
                info_text += f"File: {os.path.basename(file_path)}\n"
                info_text += f"Rows: {len(new_data):,}\n"
                info_text += f"Columns: {len(new_data.columns)}\n"
                info_text += f"Columns: {', '.join(new_data.columns[:5])}"
                if len(new_data.columns) > 5:
                    info_text += "..."
                
                messagebox.showinfo("Data Loaded", info_text, parent=parent_window)
                
                # Determine data type and update accordingly
                filename = os.path.basename(file_path).lower()
                if 'crop' in filename and 'recommendation' in filename:
                    self.data['crop_recommendation'] = new_data
                elif 'fertilizer' in filename:
                    self.data['fertilizer'] = new_data
                elif 'yield' in filename:
                    self.data['yield'] = new_data
                else:
                    # Generic data loading
                    data_name = os.path.splitext(os.path.basename(file_path))[0]
                    self.data[data_name] = new_data
                
                self.update_data_info()
                return True, f"Data loaded from {os.path.basename(file_path)}"
                
        except Exception as e:
            error_msg = f"Failed to load data: {str(e)}"
            if parent_window:
                messagebox.showerror("Error", error_msg, parent=parent_window)
            return False, error_msg
        
        return False, "No file selected"
    
    def export_data(self, data_to_export=None, parent_window=None):
        """Export data to CSV file"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save results",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                parent=parent_window
            )
            
            if file_path:
                if data_to_export is None:
                    # Create a summary report
                    report_data = {
                        'Dataset': [],
                        'Samples': [],
                        'Features': [],
                        'Status': [],
                        'Last_Updated': []
                    }
                    
                    for name, info in self.data_info.items():
                        report_data['Dataset'].append(name.replace('_', ' ').title())
                        report_data['Samples'].append(info['samples'])
                        report_data['Features'].append(info['features'])
                        report_data['Status'].append(info['status'])
                        report_data['Last_Updated'].append(info['last_updated'])
                    
                    report_df = pd.DataFrame(report_data)
                    report_df.to_csv(file_path, index=False)
                else:
                    # Export specific data
                    data_to_export.to_csv(file_path, index=False)
                
                success_msg = f"Data exported to {os.path.basename(file_path)}"
                if parent_window:
                    messagebox.showinfo("Export Successful", success_msg, parent=parent_window)
                return True, success_msg
                
        except Exception as e:
            error_msg = f"Failed to export data: {str(e)}"
            if parent_window:
                messagebox.showerror("Error", error_msg, parent=parent_window)
            return False, error_msg
        
        return False, "No file selected"
    
    def export_predictions(self, predictions_data, parent_window=None):
        """Export predictions to CSV file"""
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save predictions",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                parent=parent_window
            )
            
            if file_path:
                # Convert predictions to DataFrame
                predictions_df = pd.DataFrame(predictions_data)
                predictions_df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                predictions_df.to_csv(file_path, index=False)
                
                success_msg = f"Predictions exported to {os.path.basename(file_path)}"
                if parent_window:
                    messagebox.showinfo("Export Successful", success_msg, parent=parent_window)
                return True, success_msg
                
        except Exception as e:
            error_msg = f"Failed to export predictions: {str(e)}"
            if parent_window:
                messagebox.showerror("Error", error_msg, parent=parent_window)
            return False, error_msg
        
        return False, "No file selected"
    
    def get_data_summary(self):
        """Get summary of all datasets"""
        summary = {}
        for name, df in self.data.items():
            summary[name] = {
                'shape': df.shape,
                'columns': list(df.columns),
                'dtypes': df.dtypes.to_dict(),
                'missing_values': df.isnull().sum().to_dict(),
                'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
                'categorical_columns': df.select_dtypes(include=['object']).columns.tolist()
            }
        return summary
    
    def validate_data_for_training(self):
        """Validate if data is suitable for training"""
        validation_results = {}
        
        required_datasets = ['crop_recommendation', 'fertilizer', 'yield']
        
        for dataset_name in required_datasets:
            if dataset_name not in self.data:
                validation_results[dataset_name] = {
                    'valid': False,
                    'message': f"Dataset '{dataset_name}' not found"
                }
                continue
            
            df = self.data[dataset_name]
            
            # Check if dataset has minimum required samples
            if len(df) < 50:
                validation_results[dataset_name] = {
                    'valid': False,
                    'message': f"Dataset has only {len(df)} samples. Minimum 50 required."
                }
                continue
            
            # Check for required columns based on dataset type
            required_columns = self._get_required_columns(dataset_name)
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                validation_results[dataset_name] = {
                    'valid': False,
                    'message': f"Missing required columns: {missing_columns}"
                }
                continue
            
            # Check for excessive missing values
            missing_percentage = (df.isnull().sum() / len(df) * 100).max()
            if missing_percentage > 20:
                validation_results[dataset_name] = {
                    'valid': False,
                    'message': f"Dataset has {missing_percentage:.1f}% missing values in some columns"
                }
                continue
            
            validation_results[dataset_name] = {
                'valid': True,
                'message': "Dataset is valid for training"
            }
        
        return validation_results
    
    def _get_required_columns(self, dataset_name):
        """Get required columns for each dataset type"""
        required_columns = {
            'crop_recommendation': ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'],
            'fertilizer': ['temperature', 'humidity', 'moisture', 'soil_type', 'crop_type', 
                          'nitrogen', 'phosphorous', 'potassium', 'fertilizer'],
            'yield': ['state', 'district', 'season', 'crop', 'area', 'production', 'yield']
        }
        return required_columns.get(dataset_name, [])
    
    def backup_data(self, backup_dir=None):
        """Create backup of current data"""
        try:
            if backup_dir is None:
                backup_dir = filedialog.askdirectory(title="Select backup directory")
            
            if backup_dir:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                
                for name, df in self.data.items():
                    backup_filename = f"{name}_backup_{timestamp}.csv"
                    backup_path = os.path.join(backup_dir, backup_filename)
                    df.to_csv(backup_path, index=False)
                
                return True, f"Data backed up to {backup_dir}"
            
        except Exception as e:
            return False, f"Backup failed: {str(e)}"
        
        return False, "No backup directory selected"
    
    def get_dataset_info(self):
        """Get formatted dataset information for display"""
        info_list = []
        for name, info in self.data_info.items():
            info_list.append([
                name.replace('_', ' ').title(),
                f"{info['samples']:,}",
                str(info['features']),
                info['status']
            ])
        return info_list