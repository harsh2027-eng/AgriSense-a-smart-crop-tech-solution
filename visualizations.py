# visualizations.py - Data Visualization Components

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import numpy as np
import pandas as pd

class CropVisualizations:
    def __init__(self, chart_frame):
        self.chart_frame = chart_frame
        
    def clear_chart(self):
        """Clear previous charts"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
    
    def embed_chart(self, fig):
        """Embed matplotlib figure in tkinter"""
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def show_crop_distribution(self, data):
        """Show crop distribution chart"""
        self.clear_chart()
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.patch.set_facecolor('white')
        
        # Crop distribution pie chart
        crop_counts = data['crop_recommendation']['label'].value_counts()
        colors = plt.cm.Set3(np.linspace(0, 1, len(crop_counts)))
        
        ax1.pie(crop_counts.values, labels=crop_counts.index, autopct='%1.1f%%', 
               colors=colors, startangle=90)
        ax1.set_title('Crop Distribution', fontsize=14, fontweight='bold')
        
        # Fertilizer distribution bar chart
        fert_counts = data['fertilizer']['fertilizer'].value_counts()
        bars = ax2.bar(fert_counts.index, fert_counts.values, 
                      color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        ax2.set_title('Fertilizer Distribution', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Fertilizer Type')
        ax2.set_ylabel('Count')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        self.embed_chart(fig)
    
    def show_parameter_analysis(self, data):
        """Show parameter correlation analysis"""
        self.clear_chart()
        
        # Create figure
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('white')
        
        crop_data = data['crop_recommendation']
        
        # Temperature vs Humidity scatter plot
        scatter = ax1.scatter(crop_data['temperature'], crop_data['humidity'], 
                            c=crop_data['rainfall'], cmap='viridis', alpha=0.6)
        ax1.set_xlabel('Temperature (°C)')
        ax1.set_ylabel('Humidity (%)')
        ax1.set_title('Temperature vs Humidity (colored by Rainfall)')
        plt.colorbar(scatter, ax=ax1, label='Rainfall (mm)')
        
        # NPK levels comparison
        nutrients = ['N', 'P', 'K']
        means = [crop_data[nutrient].mean() for nutrient in nutrients]
        bars = ax2.bar(nutrients, means, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        ax2.set_title('Average NPK Levels')
        ax2.set_ylabel('Level')
        
        # Add value labels
        for bar, mean in zip(bars, means):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                    f'{mean:.1f}', ha='center', va='bottom')
        
        # pH distribution histogram
        ax3.hist(crop_data['ph'], bins=20, color='#96CEB4', alpha=0.7, edgecolor='black')
        ax3.set_xlabel('pH Level')
        ax3.set_ylabel('Frequency')
        ax3.set_title('pH Distribution')
        ax3.axvline(crop_data['ph'].mean(), color='red', linestyle='--', 
                   label=f'Mean: {crop_data["ph"].mean():.2f}')
        ax3.legend()
        
        # Rainfall by crop type
        crop_rainfall = crop_data.groupby('label')['rainfall'].mean().sort_values()
        bars = ax4.barh(crop_rainfall.index, crop_rainfall.values, 
                       color=plt.cm.Set2(np.linspace(0, 1, len(crop_rainfall))))
        ax4.set_xlabel('Average Rainfall (mm)')
        ax4.set_title('Average Rainfall by Crop')
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, crop_rainfall.values)):
            ax4.text(value + 2, i, f'{value:.1f}', va='center')
        
        plt.tight_layout()
        self.embed_chart(fig)
    
    def show_yield_trends(self, data):
        """Show yield trends analysis"""
        self.clear_chart()
        
        # Create figure
        fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, figsize=(18, 10))
        fig.patch.set_facecolor('white')
        
        yield_data = data['yield']
        
        # Yield by state
        state_yield = yield_data.groupby('state')['yield'].mean().sort_values(ascending=False)
        bars = ax1.bar(state_yield.index, state_yield.values, 
                      color='#FF6B6B', alpha=0.7)
        ax1.set_title('Average Yield by State')
        ax1.set_ylabel('Yield (tons/hectare)')
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, value in zip(bars, state_yield.values):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                    f'{value:.2f}', ha='center', va='bottom')
        
        # Yield by district (top 10)
        district_yield = yield_data.groupby('district')['yield'].mean().sort_values(ascending=False).head(10)
        bars = ax2.barh(district_yield.index, district_yield.values, 
                      color='#4ECDC4', alpha=0.7)
        ax2.set_title('Top 10 Districts by Yield')
        ax2.set_xlabel('Yield (tons/hectare)')
        
        # Yield by crop
        crop_yield = yield_data.groupby('crop')['yield'].mean().sort_values(ascending=False)
        bars = ax3.bar(crop_yield.index, crop_yield.values, 
                      color='#4ECDC4', alpha=0.7)
        ax3.set_title('Average Yield by Crop')
        ax3.set_ylabel('Yield (tons/hectare)')
        ax3.tick_params(axis='x', rotation=45)
        
        # Add value labels
        for bar, value in zip(bars, crop_yield.values):
            ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                    f'{value:.2f}', ha='center', va='bottom')
        
        # Yield by season
        season_yield = yield_data.groupby('season')['yield'].mean()
        colors = ['#45B7D1', '#96CEB4', '#FFEAA7']
        ax4.pie(season_yield.values, labels=season_yield.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
        ax4.set_title('Yield Distribution by Season')
        
        # Production vs Area scatter plot
        scatter = ax5.scatter(yield_data['area'], yield_data['production'], 
                            c=yield_data['yield'], cmap='viridis', alpha=0.6)
        ax5.set_xlabel('Area (hectares)')
        ax5.set_ylabel('Production (tons)')
        ax5.set_title('Production vs Area (colored by Yield)')
        plt.colorbar(scatter, ax=ax5, label='Yield (tons/hectare)')
        
        # Hide the 6th subplot
        ax6.set_visible(False)
        
        plt.tight_layout()
        self.embed_chart(fig)
    
    def show_feature_importance(self, model, feature_names, model_name):
        """Show feature importance for a given model"""
        self.clear_chart()
        
        if hasattr(model, 'feature_importances_'):
            fig, ax = plt.subplots(1, 1, figsize=(10, 6))
            fig.patch.set_facecolor('white')
            
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            
            # Plot feature importances
            bars = ax.bar(range(len(importances)), importances[indices],
                         color='#3498db', alpha=0.7)
            ax.set_title(f'Feature Importance - {model_name}', fontsize=14, fontweight='bold')
            ax.set_ylabel('Importance')
            ax.set_xlabel('Features')
            ax.set_xticks(range(len(importances)))
            ax.set_xticklabels([feature_names[i] for i in indices], rotation=45)
            
            # Add value labels
            for bar, importance in zip(bars, importances[indices]):
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                       f'{importance:.3f}', ha='center', va='bottom')
            
            plt.tight_layout()
            self.embed_chart(fig)