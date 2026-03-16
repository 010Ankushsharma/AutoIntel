"""
Car Price Prediction Flask Web Application
This application provides a web interface for predicting car prices using a trained ML model.
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import joblib
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'car_price_prediction_secret_key_2024'

# Global variables to store model and preprocessing objects
model = None
feature_columns = None
model_info = None


def load_model_and_preprocessors():
    """Load the trained model and preprocessing objects."""
    global model, feature_columns, model_info
    
    try:
        # Load the model
        model_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'car_price_model.pkl')
        print(f"Loading model from: {model_path}")
        model = joblib.load(model_path)
        
        # Load feature columns
        columns_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'feature_columns.pkl')
        print(f"Loading feature columns from: {columns_path}")
        feature_columns_data = joblib.load(columns_path)
        
        # Convert to list if it's an array or other type
        if hasattr(feature_columns_data, 'tolist'):
            feature_columns = feature_columns_data.tolist()
        elif isinstance(feature_columns_data, (tuple, set)):
            feature_columns = list(feature_columns_data)
        else:
            feature_columns = feature_columns_data
        
        print(f"Feature columns loaded: {len(feature_columns)} features")
        
        # Load model info
        info_path = os.path.join(os.path.dirname(__file__), '..', 'model', 'model_info.pkl')
        model_info = joblib.load(info_path)
        
        print("✓ Model and preprocessors loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return False


def prepare_input_data(input_dict):
    """Prepare input data for model prediction."""
    global feature_columns
    
    # Check if feature_columns is loaded
    if feature_columns is None or len(feature_columns) == 0:
        raise ValueError("Model feature columns not loaded. Please restart the server.")
    
    # Create a DataFrame with all features initialized to 0 or appropriate defaults
    input_df = pd.DataFrame(np.zeros((1, len(feature_columns))), columns=feature_columns)
    
    # Set the provided values
    for key, value in input_dict.items():
        if key in input_df.columns:
            input_df[key] = value
    
    return input_df


@app.route('/')
def index():
    """Render the main page with the input form."""
    return render_template('index-premium.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Verify model is loaded
        if model is None or feature_columns is None:
            error_message = "Model not loaded. Please restart the server."
            print(error_message)
            return render_template('index-premium.html', error=error_message)
        
        # Get form data
        year = int(request.form.get('year', 2020))
        km_driven = float(request.form.get('km_driven', 0))
        fuel = request.form.get('fuel', 'Petrol')
        seller_type = request.form.get('seller_type', 'Individual')
        transmission = request.form.get('transmission', 'Manual')
        owner = request.form.get('owner', 'First_Owner')
        brand = request.form.get('brand', 'Maruti Suzuki')
        engine = float(request.form.get('engine', 0))
        mileage = float(request.form.get('mileage', 0))
        max_power = float(request.form.get('max_power', 0))
        seats = int(request.form.get('seats', 5))
        
        # Map brand names to match training data
        brand_mapping = {
            'Maruti': 'Maruti Suzuki',
            'Land Rover': 'Land Rover',
            'Mini': 'MINI'
        }
        brand = brand_mapping.get(brand, brand)
        
        # Prepare input dictionary
        input_dict = {
            'year': year,
            'km_driven': km_driven,
            'engine': engine,
            'mileage': mileage,
            'max_power': max_power,
            'seats': seats,
            f'fuel_{fuel}': 1,
            f'seller_type_{seller_type}': 1,
            f'transmission_{transmission}': 1,
            f'owner_{owner}': 1,
            f'brand_{brand}': 1
        }
        
        # Prepare data for prediction
        input_df = prepare_input_data(input_dict)
        
        # Make prediction
        prediction = model.predict(input_df)
        predicted_price = max(0, prediction[0])  # Ensure non-negative
        
        # Calculate price ranges (±20% for low/high estimates)
        low_range = predicted_price * 0.8
        high_range = predicted_price * 1.2
        
        # Format the results
        result = {
            'predicted_price': round(predicted_price, 2),
            'low_range': round(low_range, 2),
            'high_range': round(high_range, 2),
            'success': True
        }
        
        return render_template('result-premium.html', result=result, input_data=request.form)
        
    except Exception as e:
        error_message = f"Error during prediction: {str(e)}"
        print(error_message)
        import traceback
        traceback.print_exc()
        return render_template('index-premium.html', error=error_message)


@app.route('/predict_api', methods=['POST'])
def predict_api():
    """API endpoint for predictions (returns JSON)."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided', 'success': False}), 400
        
        # Extract features from JSON
        input_dict = {}
        
        # Numerical features
        numerical_features = ['year', 'km_driven', 'engine', 'mileage', 'max_power', 'seats']
        for feature in numerical_features:
            input_dict[feature] = float(data.get(feature, 0))
        
        # Categorical features - create one-hot encoded columns
        categorical_mappings = {
            'fuel': ['Petrol', 'Diesel', 'CNG', 'Electric', 'LPG'],
            'seller_type': ['Individual', 'Dealer', 'Trustmark Dealer'],
            'transmission': ['Manual', 'Automatic'],
            'owner': ['First_Owner', 'Second_Owner', 'Third_Owner', 'Fourth_Owner Or More'],
            'brand': ['Maruti', 'Hyundai', 'Honda', 'Toyota', 'Mahindra', 'Tata', 
                     'Ford', 'Chevrolet', 'Volkswagen', 'BMW', 'Mercedes-Benz', 
                     'Audi', 'Skoda', 'Nissan', 'Renault', 'Jaguar', 'Volvo', 
                     'Fiat', 'Jeep', 'Mini', 'Land', 'Kia', 'MG', 'Datsun', 'Force']
        }
        
        for category, options in categorical_mappings.items():
            selected_value = data.get(category, options[0])
            for option in options:
                col_name = f'{category}_{option}'
                input_dict[col_name] = 1 if option == selected_value else 0
        
        # Prepare data for prediction
        input_df = prepare_input_data(input_dict)
        
        # Make prediction
        prediction = model.predict(input_df)
        predicted_price = max(0, prediction[0])
        
        # Calculate price ranges
        low_range = predicted_price * 0.8
        high_range = predicted_price * 1.2
        
        result = {
            'predicted_price': round(predicted_price, 2),
            'currency': 'INR',
            'low_range': round(low_range, 2),
            'high_range': round(high_range, 2),
            'success': True,
            'message': 'Prediction successful'
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


# Load model on startup
if __name__ == '__main__':
    print("="*60)
    print("CAR PRICE PREDICTION WEB APPLICATION")
    print("="*60)
    print("\nStarting Flask server...")
    
    # Load model and preprocessors
    if load_model_and_preprocessors():
        print(f"✓ Model Name: {model_info['model_name']}")
        print(f"✓ R² Score: {model_info['r2_score']:.4f}")
        print(f"✓ Features: {model_info['feature_count']}")
        print("\n" + "="*60)
        print("Server is ready!")
        print("Open your browser to: http://127.0.0.1:5000/")
        print("="*60)
    else:
        print("\n⚠ WARNING: Model could not be loaded.")
        print("Please run 'python model/train_model.py' first to train the model.")
        print("="*60)
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
