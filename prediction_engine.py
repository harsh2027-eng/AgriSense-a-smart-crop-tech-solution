# prediction_engine.py - Prediction Logic and Results

from config import CROP_INFO, FERTILIZER_INFO, YIELD_RECOMMENDATIONS, DEFAULT_RECOMMENDATIONS

class PredictionEngine:
    def __init__(self, ml_models):
        self.ml_models = ml_models
    
    def format_crop_results(self, prediction_data, inputs):
        """Format crop recommendation results"""
        prediction = prediction_data['prediction']
        confidence = prediction_data['confidence']
        all_probabilities = prediction_data['all_probabilities']
        
        result_text = f"🌱 CROP RECOMMENDATION RESULTS\n"
        result_text += "=" * 50 + "\n\n"
        result_text += f"📍 RECOMMENDED CROP: {prediction.upper()}\n"
        result_text += f"🎯 Confidence: {confidence*100:.1f}%\n\n"
        
        result_text += "📊 ALL CROP SUITABILITY SCORES:\n"
        result_text += "-" * 30 + "\n"
        for crop, prob in all_probabilities:
            result_text += f"{crop.capitalize():12} | {prob*100:6.1f}%\n"
        
        result_text += "\n💡 RECOMMENDATIONS:\n"
        result_text += "-" * 20 + "\n"
        
        # Add specific recommendations based on the predicted crop
        recommendations = CROP_INFO.get(prediction, {}).get('recommendations', [
            "• Follow standard cultivation practices",
            "• Monitor crop regularly", 
            "• Maintain soil health"
        ])
        
        for rec in recommendations:
            result_text += rec + "\n"
        
        return result_text
    
    def format_fertilizer_results(self, prediction_data, categorical_inputs, numeric_inputs):
        """Format fertilizer recommendation results"""
        prediction = prediction_data['prediction']
        
        result_text = f"🧪 FERTILIZER RECOMMENDATION\n"
        result_text += "=" * 50 + "\n\n"
        result_text += f"📍 RECOMMENDED FERTILIZER: {prediction}\n\n"
        
        # Add fertilizer information
        if prediction in FERTILIZER_INFO:
            info = FERTILIZER_INFO[prediction]
            result_text += f"🔬 COMPOSITION: {info['composition']}\n\n"
            result_text += f"✅ BENEFITS:\n{info['benefits']}\n\n"
            result_text += f"📅 APPLICATION:\n{info['application']}\n\n"
        
        # Add nutrient analysis
        result_text += "📊 NUTRIENT ANALYSIS:\n"
        result_text += "-" * 25 + "\n"
        
        # Analyze nutrient levels
        n_level = self._get_nutrient_level(numeric_inputs['nitrogen'])
        p_level = self._get_nutrient_level(numeric_inputs['phosphorous'])
        k_level = self._get_nutrient_level(numeric_inputs['potassium'])
        
        result_text += f"Nitrogen (N):     {numeric_inputs['nitrogen']:.1f} - {n_level}\n"
        result_text += f"Phosphorous (P):  {numeric_inputs['phosphorous']:.1f} - {p_level}\n"
        result_text += f"Potassium (K):    {numeric_inputs['potassium']:.1f} - {k_level}\n\n"
        
        # Add specific recommendations
        result_text += "💡 SPECIFIC RECOMMENDATIONS:\n"
        result_text += "-" * 30 + "\n"
        
        if n_level == "Low":
            result_text += "• Nitrogen deficiency detected - increase nitrogen-rich fertilizers\n"
        if p_level == "Low":
            result_text += "• Phosphorous deficiency detected - apply phosphatic fertilizers\n"
        if k_level == "Low":
            result_text += "• Potassium deficiency detected - apply potash fertilizers\n"
        
        result_text += f"• Soil type: {categorical_inputs['soil_type']} - adjust application accordingly\n"
        result_text += f"• Crop: {categorical_inputs['crop_type']} - follow crop-specific guidelines\n"
        
        return result_text
    
    def format_yield_results(self, prediction_data, categorical_inputs, numeric_inputs):
        """Format yield prediction results"""
        predicted_yield = prediction_data['prediction']
        current_yield = numeric_inputs['production'] / numeric_inputs['area']
        
        result_text = f"📊 YIELD PREDICTION RESULTS\n"
        result_text += "=" * 50 + "\n\n"
        result_text += f"📍 LOCATION: {categorical_inputs['state']}, {categorical_inputs['district']}\n"
        result_text += f"🌾 CROP: {categorical_inputs['crop']} ({categorical_inputs['season']} season)\n"
        result_text += f"📏 AREA: {numeric_inputs['area']:,.0f} hectares\n\n"
        
        result_text += "📈 YIELD ANALYSIS:\n"
        result_text += "-" * 20 + "\n"
        result_text += f"Current Yield:    {current_yield:.2f} tons/hectare\n"
        result_text += f"Predicted Yield:  {predicted_yield:.2f} tons/hectare\n"
        
        # Calculate difference
        difference = predicted_yield - current_yield
        percentage_change = (difference / current_yield) * 100 if current_yield > 0 else 0
        
        result_text += f"Difference:       {difference:+.2f} tons/hectare\n"
        result_text += f"Change:           {percentage_change:+.1f}%\n\n"
        
        # Add interpretation
        if percentage_change > 10:
            result_text += "✅ EXCELLENT: Yield is expected to be significantly higher!\n"
        elif percentage_change > 0:
            result_text += "✅ GOOD: Yield is expected to be higher than current level.\n"
        elif percentage_change > -10:
            result_text += "⚠️  CAUTION: Yield is expected to be slightly lower.\n"
        else:
            result_text += "❌ CONCERN: Yield is expected to be significantly lower.\n"
        
        result_text += "\n💡 RECOMMENDATIONS:\n"
        result_text += "-" * 20 + "\n"
        
        # Add crop-specific recommendations
        recommendations = YIELD_RECOMMENDATIONS.get(
            categorical_inputs['crop'], 
            DEFAULT_RECOMMENDATIONS
        )
        
        for rec in recommendations:
            result_text += rec + "\n"
        
        return result_text
    
    def _get_nutrient_level(self, value):
        """Get nutrient level description"""
        if value > 70:
            return "High"
        elif value > 30:
            return "Medium"
        else:
            return "Low"
    
    def predict_crop(self, inputs):
        """Predict crop recommendation with formatted results"""
        try:
            prediction_data = self.ml_models.predict_crop(inputs)
            formatted_results = self.format_crop_results(prediction_data, inputs)
            return {
                'success': True,
                'results': formatted_results,
                'prediction': prediction_data['prediction']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_fertilizer(self, categorical_inputs, numeric_inputs):
        """Predict fertilizer recommendation with formatted results"""
        try:
            # Prepare inputs for model
            inputs = [
                numeric_inputs['temperature'], 
                numeric_inputs['humidity'], 
                numeric_inputs['moisture']
            ]
            inputs.append(categorical_inputs['soil_type'])
            inputs.append(categorical_inputs['crop_type'])
            inputs.extend([
                numeric_inputs['nitrogen'], 
                numeric_inputs['phosphorous'], 
                numeric_inputs['potassium']
            ])
            
            # Encode categorical inputs
            encoded_inputs = self.ml_models.encode_categorical_inputs(inputs, 'fertilizer')
            prediction_data = self.ml_models.predict_fertilizer(encoded_inputs)
            formatted_results = self.format_fertilizer_results(
                prediction_data, categorical_inputs, numeric_inputs
            )
            
            return {
                'success': True,
                'results': formatted_results,
                'prediction': prediction_data['prediction']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def predict_yield(self, categorical_inputs, numeric_inputs):
        """Predict yield with formatted results"""
        try:
            # Prepare inputs for model
            inputs = [
                categorical_inputs['state'],
                categorical_inputs['district'],
                categorical_inputs['season'],
                categorical_inputs['crop'],
                numeric_inputs['area'],
                numeric_inputs['production']
            ]
            
            # Encode categorical inputs
            encoded_inputs = self.ml_models.encode_categorical_inputs(inputs, 'yield')
            prediction_data = self.ml_models.predict_yield(encoded_inputs)
            formatted_results = self.format_yield_results(
                prediction_data, categorical_inputs, numeric_inputs
            )
            
            return {
                'success': True,
                'results': formatted_results,
                'prediction': prediction_data['prediction']
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }