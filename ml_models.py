# ml_models.py - Machine Learning Models

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error
from config import MODEL_CONFIG
import warnings
warnings.filterwarnings('ignore')

class CropMLModels:
    def __init__(self):
        self.models = {}
        self.encoders = {}
        self.model_config = MODEL_CONFIG
    
    def train_crop_model(self, data):
        """Train crop recommendation model"""
        X = data.drop('label', axis=1)
        y = data['label']
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.model_config['test_size'], 
            random_state=self.model_config['random_state']
        )
        
        self.models['crop'] = RandomForestClassifier(
            n_estimators=self.model_config['n_estimators'],
            random_state=self.model_config['random_state']
        )
        self.models['crop'].fit(X_train, y_train)
        
        # Calculate accuracy
        train_accuracy = self.models['crop'].score(X_train, y_train)
        test_accuracy = self.models['crop'].score(X_test, y_test)
        
        return {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'model': self.models['crop']
        }
    
    def train_fertilizer_model(self, data):
        """Train fertilizer recommendation model"""
        X = data.drop('fertilizer', axis=1)
        y = data['fertilizer']
        
        # Encode categorical variables
        self.encoders['soil_type'] = LabelEncoder()
        self.encoders['crop_type'] = LabelEncoder()
        
        X_encoded = X.copy()
        X_encoded['soil_type'] = self.encoders['soil_type'].fit_transform(X['soil_type'])
        X_encoded['crop_type'] = self.encoders['crop_type'].fit_transform(X['crop_type'])
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y,
            test_size=self.model_config['test_size'],
            random_state=self.model_config['random_state']
        )
        
        self.models['fertilizer'] = RandomForestClassifier(
            n_estimators=self.model_config['n_estimators'],
            random_state=self.model_config['random_state']
        )
        self.models['fertilizer'].fit(X_train, y_train)
        
        train_accuracy = self.models['fertilizer'].score(X_train, y_train)
        test_accuracy = self.models['fertilizer'].score(X_test, y_test)
        
        return {
            'train_accuracy': train_accuracy,
            'test_accuracy': test_accuracy,
            'model': self.models['fertilizer']
        }
    
    def train_yield_model(self, data):
        """Train yield prediction model"""
        X = data.drop('yield', axis=1)
        y = data['yield']
        
        # Encode categorical variables
        self.encoders['state'] = LabelEncoder()
        self.encoders['district'] = LabelEncoder()
        self.encoders['season'] = LabelEncoder()
        self.encoders['crop_yield'] = LabelEncoder()
        
        X_encoded = X.copy()
        X_encoded['state'] = self.encoders['state'].fit_transform(X['state'])
        X_encoded['district'] = self.encoders['district'].fit_transform(X['district'])
        X_encoded['season'] = self.encoders['season'].fit_transform(X['season'])
        X_encoded['crop'] = self.encoders['crop_yield'].fit_transform(X['crop'])
        
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y,
            test_size=self.model_config['test_size'],
            random_state=self.model_config['random_state']
        )
        
        self.models['yield'] = RandomForestRegressor(
            n_estimators=self.model_config['n_estimators'],
            random_state=self.model_config['random_state']
        )
        self.models['yield'].fit(X_train, y_train)
        
        train_score = self.models['yield'].score(X_train, y_train)
        test_score = self.models['yield'].score(X_test, y_test)
        
        y_pred = self.models['yield'].predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        
        return {
            'train_score': train_score,
            'test_score': test_score,
            'mse': mse,
            'model': self.models['yield']
        }
    
    def train_all_models(self, data):
        """Train all models"""
        results = {}
        
        # Train crop model
        results['crop'] = self.train_crop_model(data['crop_recommendation'])
        
        # Train fertilizer model
        results['fertilizer'] = self.train_fertilizer_model(data['fertilizer'])
        
        # Train yield model
        results['yield'] = self.train_yield_model(data['yield'])
        
        return results
    
    def predict_crop(self, inputs):
        """Predict crop recommendation"""
        if 'crop' not in self.models:
            raise ValueError("Crop model not trained")
        
        prediction = self.models['crop'].predict([inputs])[0]
        probabilities = self.models['crop'].predict_proba([inputs])[0]
        classes = self.models['crop'].classes_
        
        crop_probs = list(zip(classes, probabilities))
        crop_probs.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'prediction': prediction,
            'confidence': max(probabilities),
            'all_probabilities': crop_probs
        }
    
    def predict_fertilizer(self, inputs):
        """Predict fertilizer recommendation"""
        if 'fertilizer' not in self.models:
            raise ValueError("Fertilizer model not trained")
        
        prediction = self.models['fertilizer'].predict([inputs])[0]
        probabilities = self.models['fertilizer'].predict_proba([inputs])[0]
        
        return {
            'prediction': prediction,
            'confidence': max(probabilities)
        }
    
    def predict_yield(self, inputs):
        """Predict crop yield"""
        if 'yield' not in self.models:
            raise ValueError("Yield model not trained")
        
        prediction = self.models['yield'].predict([inputs])[0]
        
        return {
            'prediction': prediction
        }
    
    def encode_categorical_inputs(self, inputs, model_type):
        """Encode categorical inputs for prediction"""
        if model_type == 'fertilizer':
            encoded_inputs = inputs.copy()
            encoded_inputs[3] = self.encoders['soil_type'].transform([inputs[3]])[0]
            encoded_inputs[4] = self.encoders['crop_type'].transform([inputs[4]])[0]
            return encoded_inputs
        
        elif model_type == 'yield':
            encoded_inputs = []
            encoded_inputs.append(self.encoders['state'].transform([inputs[0]])[0])
            encoded_inputs.append(self.encoders['district'].transform([inputs[1]])[0])
            encoded_inputs.append(self.encoders['season'].transform([inputs[2]])[0])
            encoded_inputs.append(self.encoders['crop_yield'].transform([inputs[3]])[0])
            encoded_inputs.extend(inputs[4:])  # Add numeric inputs
            return encoded_inputs
        
        return inputs