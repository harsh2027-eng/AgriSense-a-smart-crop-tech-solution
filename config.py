# config.py - Configuration and Constants

# Application settings
APP_CONFIG = {
    'title': "🌾 AgriSense - (A Smart Crop Tech)",
    'geometry': "1400x900",
    'min_width': 1200,
    'min_height': 800,
    'background': '#f0f8ff'
}

# Model parameters
MODEL_CONFIG = {
    'n_estimators': 100,
    'random_state': 42,
    'test_size': 0.2
}

# UI Styles
STYLES = {
    'header': {'font': ('Arial', 24, 'bold'), 'foreground': '#2c3e50'},
    'subheader': {'font': ('Arial', 14, 'bold'), 'foreground': '#34495e'},
    'info': {'font': ('Arial', 10), 'foreground': '#7f8c8d'},
    'text': {'font': ('Arial', 11)},
    'status': {'font': ('Arial', 9)}
}

# Colors
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'accent': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'background': '#f0f8ff',
    'white': '#ffffff',
    'light_gray': '#ecf0f1',
    'gray': '#7f8c8d'
}

# Data generation parameters
DATA_GENERATION = {
    'n_samples': 1000,
    'random_seed': 42
}

# Crop information
CROP_INFO = {
    'rice': {
        'recommendations': [
            "• Ensure adequate water supply",
            "• Monitor for pests regularly", 
            "• Apply nitrogen in split doses"
        ]
    },
    'wheat': {
        'recommendations': [
            "• Ensure good drainage",
            "• Apply phosphorus at sowing",
            "• Monitor for rust diseases"
        ]
    },
    'cotton': {
        'recommendations': [
            "• Maintain proper spacing",
            "• Regular pest monitoring",
            "• Adequate potash application"
        ]
    },
    'maize': {
        'recommendations': [
            "• Ensure adequate nitrogen",
            "• Maintain soil moisture",
            "• Monitor for stem borers"
        ]
    },
    'coffee': {
        'recommendations': [
            "• Provide shade",
            "• Maintain acidic soil pH",
            "• Regular pruning required"
        ]
    }
}

# Fertilizer information
FERTILIZER_INFO = {
    'Urea': {
        'composition': 'Nitrogen (46%)',
        'benefits': 'Promotes leaf growth and green color',
        'application': 'Apply in split doses during growing season'
    },
    'DAP': {
        'composition': 'Nitrogen (18%) + Phosphorus (46%)',
        'benefits': 'Promotes root development and flowering',
        'application': 'Apply at the time of sowing'
    },
    'MOP': {
        'composition': 'Potassium (60%)',
        'benefits': 'Improves disease resistance and fruit quality',
        'application': 'Apply before flowering stage'
    },
    'NPK': {
        'composition': 'Balanced N-P-K nutrients',
        'benefits': 'Complete nutrition for overall plant growth',
        'application': 'Apply as per soil test recommendations'
    }
}

# Crop-specific yield recommendations
YIELD_RECOMMENDATIONS = {
    'Rice': [
        "• Maintain optimal water levels",
        "• Apply fertilizers in split doses",
        "• Monitor for pest attacks",
        "• Ensure proper spacing"
    ],
    'Wheat': [
        "• Ensure adequate drainage",
        "• Apply phosphorus at sowing time",
        "• Monitor for rust diseases",
        "• Harvest at right moisture content"
    ],
    'Cotton': [
        "• Regular pest monitoring required",
        "• Maintain proper plant spacing",
        "• Apply potash adequately",
        "• Ensure good drainage"
    ],
    'Sugarcane': [
        "• Maintain soil moisture",
        "• Apply nitrogen in multiple doses",
        "• Control weeds effectively",
        "• Monitor for red rot disease"
    ]
}

# Default recommendations
DEFAULT_RECOMMENDATIONS = [
    "• Follow standard cultivation practices",
    "• Monitor crop health regularly",
    "• Apply fertilizers as recommended",
    "• Maintain proper irrigation"
]

# Input field definitions
CROP_INPUT_FIELDS = [
    ("Nitrogen (N)", "N"),
    ("Phosphorus (P)", "P"),
    ("Potassium (K)", "K"),
    ("Temperature (°C)", "temperature"),
    ("Humidity (%)", "humidity"),
    ("pH Level", "ph"),
    ("Rainfall (mm)", "rainfall")
]

FERTILIZER_DROPDOWN_FIELDS = [
    ("Soil Type", "soil_type", ['Sandy', 'Loamy', 'Black', 'Red', 'Clayey']),
    ("Crop Type", "crop_type", ['Maize', 'Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Wheat'])
]

FERTILIZER_NUMERIC_FIELDS = [
    ("Temperature (°C)", "temperature"),
    ("Humidity (%)", "humidity"),
    ("Soil Moisture (%)", "moisture"),
    ("Nitrogen Level", "nitrogen"),
    ("Phosphorous Level", "phosphorous"),
    ("Potassium Level", "potassium")
]

# State and District mapping
STATE_DISTRICT_MAPPING = {
    'Punjab': ['Amritsar', 'Ludhiana', 'Jalandhar', 'Patiala'],
    'Haryana': ['Gurgaon', 'Faridabad', 'Hisar', 'Rohtak'],
    'UP': ['Lucknow', 'Kanpur', 'Varanasi', 'Agra'],
    'Bihar': ['Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur'],
    'West Bengal': ['Kolkata', 'Howrah', 'Burdwan', 'Murshidabad']
}

YIELD_DROPDOWN_FIELDS = [
    ("State", "state", ['Punjab', 'Haryana', 'UP', 'Bihar', 'West Bengal']),
    ("District", "district", ['Amritsar', 'Ludhiana', 'Jalandhar', 'Patiala', 'Gurgaon', 'Faridabad', 'Hisar', 'Rohtak', 'Lucknow', 'Kanpur', 'Varanasi', 'Agra', 'Patna', 'Gaya', 'Bhagalpur', 'Muzaffarpur', 'Kolkata', 'Howrah', 'Burdwan', 'Murshidabad']),
    ("Season", "season", ['Kharif', 'Rabi', 'Whole Year']),
    ("Crop", "crop", ['Rice', 'Wheat', 'Cotton', 'Sugarcane'])
]

YIELD_NUMERIC_FIELDS = [
    ("Area (hectares)", "area"),
    ("Production (tons)", "production")
]