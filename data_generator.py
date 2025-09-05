# data_generator.py - Sample Data Generation

import pandas as pd
import numpy as np
from config import DATA_GENERATION

class DataGenerator:
    def __init__(self):
        np.random.seed(DATA_GENERATION['random_seed'])
        self.n_samples = DATA_GENERATION['n_samples']
    
    def generate_crop_data(self):
        """Generate sample crop recommendation data"""
        data = pd.DataFrame({
            'N': np.random.uniform(0, 140, self.n_samples),
            'P': np.random.uniform(5, 145, self.n_samples),
            'K': np.random.uniform(5, 205, self.n_samples),
            'temperature': np.random.uniform(8.8, 43.7, self.n_samples),
            'humidity': np.random.uniform(14.3, 99.9, self.n_samples),
            'ph': np.random.uniform(3.5, 9.9, self.n_samples),
            'rainfall': np.random.uniform(20.2, 298.6, self.n_samples)
        })
        
        # Create target labels based on conditions
        crop_labels = []
        for _, row in data.iterrows():
            if row['rainfall'] > 200:
                crop_labels.append('rice')
            elif row['temperature'] > 30:
                crop_labels.append('cotton')
            elif row['ph'] < 6:
                crop_labels.append('coffee')
            elif row['N'] > 100:
                crop_labels.append('maize')
            else:
                crop_labels.append('wheat')
        
        data['label'] = crop_labels
        return data
    
    def generate_fertilizer_data(self):
        """Generate sample fertilizer recommendation data"""
        data = pd.DataFrame({
            'temperature': np.random.uniform(15, 40, self.n_samples),
            'humidity': np.random.uniform(20, 90, self.n_samples),
            'moisture': np.random.uniform(10, 80, self.n_samples),
            'soil_type': np.random.choice(['Sandy', 'Loamy', 'Black', 'Red', 'Clayey'], self.n_samples),
            'crop_type': np.random.choice(['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Wheat'], self.n_samples),
            'nitrogen': np.random.uniform(0, 100, self.n_samples),
            'phosphorous': np.random.uniform(0, 100, self.n_samples),
            'potassium': np.random.uniform(0, 100, self.n_samples)
        })
        
        # Create fertilizer labels
        fertilizer_labels = []
        for _, row in data.iterrows():
            if row['nitrogen'] < 40:
                fertilizer_labels.append('Urea')
            elif row['phosphorous'] < 40:
                fertilizer_labels.append('DAP')
            elif row['potassium'] < 40:
                fertilizer_labels.append('MOP')
            else:
                fertilizer_labels.append('NPK')
        
        data['fertilizer'] = fertilizer_labels
        return data
    
    def generate_yield_data(self):
        """Generate sample yield prediction data"""
        # State and district mapping
        state_district_mapping = {
            'Punjab': ['Amritsar', 'Ludhiana', 'Jalandhar', 'Patiala'],
            'Haryana': ['Gurgaon', 'Faridabad', 'Hisar', 'Rohtak'],
            'UP': ['Lucknow', 'Kanpur', 'Varanasi', 'Agra'],
            'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur'],
            'West Bengal': ['Kolkata', 'Howrah', 'Burdwan', 'Murshidabad']
        }
        
        # Generate states first
        states = np.random.choice(['Punjab', 'Haryana', 'UP', 'Bihar', 'West Bengal'], self.n_samples)
        
        # Generate corresponding districts
        districts = []
        for state in states:
            districts.append(np.random.choice(state_district_mapping[state]))
        
        data = pd.DataFrame({
            'state': states,
            'district': districts,
            'season': np.random.choice(['Kharif', 'Rabi', 'Whole Year'], self.n_samples),
            'crop': np.random.choice(['Rice', 'Wheat', 'Cotton', 'Sugarcane'], self.n_samples),
            'area': np.random.uniform(1000, 50000, self.n_samples),
            'production': np.random.uniform(5000, 200000, self.n_samples)
        })
        
        data['yield'] = data['production'] / data['area']
        return data
    
    def generate_all_data(self):
        """Generate all sample datasets"""
        return {
            'crop_recommendation': self.generate_crop_data(),
            'fertilizer': self.generate_fertilizer_data(),
            'yield': self.generate_yield_data()
        }