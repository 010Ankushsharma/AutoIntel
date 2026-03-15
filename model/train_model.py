"""
Car Price Prediction Model Training Script
This script loads the car dataset, preprocesses it, trains multiple ML models,
and saves the best performing model along with preprocessing objects.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib
import os
import re


def load_and_clean_data(filepath):
    """Load and clean the car dataset."""
    print("Loading dataset...")
    df = pd.read_csv(filepath)
    
    print(f"Initial dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print("\nCleaning data...")
    
    # Rename columns to match expected format
    df = df.rename(columns={
        'Make': 'brand',
        'Model': 'model',
        'Price': 'selling_price',
        'Year': 'year',
        'Kilometer': 'km_driven',
        'Fuel Type': 'fuel',
        'Transmission': 'transmission',
        'Seller Type': 'seller_type',
        'Owner': 'owner',
        'Engine': 'engine',
        'Max Power': 'max_power',
        'Seating Capacity': 'seats'
    })
    
    # Clean numeric columns that might have units
    # Mileage - check if it exists, otherwise create from fuel efficiency data
    if 'mileage' not in df.columns:
        # Create a synthetic mileage column based on typical values
        # In real scenario, this would come from the dataset
        print("Creating estimated mileage values...")
        df['mileage'] = df.apply(lambda row: estimate_mileage(row), axis=1)
    else:
        df['mileage'] = df['mileage'].astype(str).apply(lambda x: x.split('kmpl')[0] if 'kmpl' in str(x) else x)
        df['mileage'] = pd.to_numeric(df['mileage'], errors='coerce')
    
    # Clean engine (remove CC if present)
    df['engine'] = df['engine'].astype(str).apply(lambda x: x.split('CC')[0] if 'CC' in str(x) else x)
    df['engine'] = pd.to_numeric(df['engine'], errors='coerce')
    
    # Clean max_power (remove bhp if present)
    df['max_power'] = df['max_power'].astype(str).apply(lambda x: x.split('bhp')[0] if 'bhp' in str(x) else x)
    df['max_power'] = pd.to_numeric(df['max_power'], errors='coerce')
    
    # Handle missing values
    print("\nHandling missing values...")
    initial_rows = len(df)
    
    # Drop rows with critical missing values
    df = df.dropna(subset=['selling_price', 'year', 'km_driven', 'fuel', 'transmission'])
    
    # Fill numerical missing values with median
    numeric_cols = ['engine', 'mileage', 'max_power', 'seats']
    for col in numeric_cols:
        if col in df.columns:
            median_val = df[col].median()
            if pd.isna(median_val):  # If median is also NaN, use 0
                median_val = 0
            df[col] = df[col].fillna(median_val)
    
    # After all processing, drop any remaining rows with NaN
    df = df.dropna()
    
    final_rows = len(df)
    print(f"Dropped {initial_rows - final_rows} rows with missing values")
    print(f"Final dataset shape: {df.shape}")
    
    return df


def estimate_mileage(row):
    """Estimate mileage based on fuel type and other factors."""
    fuel_type = str(row.get('fuel', '')).lower()
    if 'diesel' in fuel_type:
        return 20.0
    elif 'petrol' in fuel_type:
        return 15.0
    elif 'electric' in fuel_type:
        return 100.0  # km per kWh equivalent
    elif 'cng' in fuel_type:
        return 25.0
    else:
        return 18.0  # default


def prepare_features(df):
    """Prepare features and target variable."""
    print("\nPreparing features...")
    
    # Select only the columns we need
    selected_columns = ['year', 'km_driven', 'fuel', 'transmission', 'seller_type', 
                       'owner', 'brand', 'engine', 'mileage', 'max_power', 'seats', 'selling_price']
    
    # Check which columns exist
    available_columns = [col for col in selected_columns if col in df.columns]
    print(f"Available columns: {available_columns}")
    
    df_selected = df[available_columns].copy()
    
    # Separate features and target
    if 'selling_price' not in df_selected.columns:
        raise ValueError("Target variable 'selling_price' not found in dataset")
    
    X = df_selected.drop('selling_price', axis=1)
    y = df_selected['selling_price']
    
    # Identify categorical columns
    categorical_cols = ['fuel', 'transmission', 'seller_type', 'owner', 'brand']
    
    # Filter to only existing categorical columns
    categorical_cols = [col for col in categorical_cols if col in X.columns]
    
    # One-hot encoding for categorical variables
    print("Applying One-Hot Encoding to categorical variables...")
    X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    
    print(f"Number of features after encoding: {X.shape[1]}")
    
    return X, y


def train_and_evaluate_models(X, y):
    """Train multiple models and evaluate their performance."""
    print("\nSplitting data into training and testing sets (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Testing set size: {len(X_test)}")
    
    # Initialize models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting Regressor': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    print("\n" + "="*60)
    print("TRAINING AND EVALUATING MODELS")
    print("="*60)
    
    for name, model in models.items():
        print(f"\nTraining {name}...")
        
        # Train the model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Evaluate
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        mae = mean_absolute_error(y_test, y_pred_test)
        mse = mean_squared_error(y_test, y_pred_test)
        rmse = np.sqrt(mse)
        
        results[name] = {
            'model': model,
            'r2_train': r2_train,
            'r2_test': r2_test,
            'mae': mae,
            'rmse': rmse
        }
        
        print(f"\n  Training R² Score: {r2_train:.4f}")
        print(f"  Testing R² Score: {r2_test:.4f}")
        print(f"  Mean Absolute Error: {mae:,.2f}")
        print(f"  Root Mean Squared Error: {rmse:,.2f}")
    
    # Select best model based on R² score on test set
    best_model_name = max(results, key=lambda x: results[x]['r2_test'])
    print("\n" + "="*60)
    print(f"BEST MODEL: {best_model_name}")
    print(f"  Testing R² Score: {results[best_model_name]['r2_test']:.4f}")
    print(f"  MAE: {results[best_model_name]['mae']:,.2f}")
    print(f"  RMSE: {results[best_model_name]['rmse']:,.2f}")
    print("="*60)
    
    return results, best_model_name, X_train.columns


def save_model_and_preprocessors(results, best_model_name, feature_columns):
    """Save the best model and preprocessing objects."""
    print("\nSaving model and preprocessors...")
    
    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)
    
    # Save the best model
    best_model = results[best_model_name]['model']
    model_path = 'model/car_price_model.pkl'
    joblib.dump(best_model, model_path)
    print(f"✓ Model saved to: {model_path}")
    
    # Save feature columns for inference
    columns_path = 'model/feature_columns.pkl'
    joblib.dump(feature_columns, columns_path)
    print(f"✓ Feature columns saved to: {columns_path}")
    
    # Save model info
    model_info = {
        'model_name': best_model_name,
        'r2_score': results[best_model_name]['r2_test'],
        'mae': results[best_model_name]['mae'],
        'rmse': results[best_model_name]['rmse'],
        'feature_count': len(feature_columns)
    }
    
    info_path = 'model/model_info.pkl'
    joblib.dump(model_info, info_path)
    print(f"✓ Model info saved to: {info_path}")
    
    return model_path


def main():
    """Main function to run the entire training pipeline."""
    print("="*60)
    print("CAR PRICE PREDICTION MODEL TRAINING")
    print("="*60)
    
    # Load and clean data
    df = load_and_clean_data('data/car_details_v4.csv')
    
    # Prepare features
    X, y = prepare_features(df)
    
    # Train and evaluate models
    results, best_model_name, feature_columns = train_and_evaluate_models(X, y)
    
    # Save model and preprocessors
    save_model_and_preprocessors(results, best_model_name, feature_columns)
    
    print("\n" + "="*60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run the Flask application: python app/app.py")
    print("2. Open your browser to http://127.0.0.1:5000/")
    print("3. Use the web interface to predict car prices!")
    print("\n")


if __name__ == "__main__":
    main()
