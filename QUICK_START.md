# 🚗 AutoIntel - Quick Start Guide

## Installation & Setup (5 minutes)

### Step 1: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Train the ML Model
```powershell
python model\train_model.py
```

This will:
- Load 2,059 car records from the dataset
- Clean and preprocess the data
- Train 3 different ML models (Linear Regression, Random Forest, Gradient Boosting)
- Automatically select the best model (Gradient Boosting with 69.24% accuracy)
- Save the trained model to `model/car_price_model.pkl`

### Step 3: Start the Web Application
```powershell
python app\app.py
```

The server will start at: **http://127.0.0.1:5000/**

---

## Using the Application

### Making a Prediction

1. **Open your browser** to http://127.0.0.1:5000/

2. **Fill in the car details form**:
   - **Car Brand**: Select from dropdown (Maruti, Hyundai, Honda, Toyota, etc.)
   - **Year**: Manufacturing year (2000-2026)
   - **Kilometers Driven**: Total distance covered
   - **Fuel Type**: Petrol, Diesel, CNG, Electric, or LPG
   - **Transmission**: Manual or Automatic
   - **Engine Capacity**: In CC (e.g., 1200)
   - **Mileage**: In kmpl (e.g., 15.0)
   - **Max Power**: In bhp (e.g., 80.0)
   - **Seats**: Number of seats (2-10)
   - **Seller Type**: Individual, Dealer, or Trustmark Dealer
   - **Owner**: First, Second, Third, or Fourth+ owner

3. **Click "Calculate Price"** button

4. **View Results**:
   - **Estimated Market Value**: Main prediction
   - **Low Range**: Conservative estimate (80% of predicted value)
   - **Average Range**: Fair market value (predicted value)
   - **High Range**: Premium listing price (120% of predicted value)

---

## Example Prediction

**Sample Input:**
- Brand: Maruti Suzuki
- Year: 2018
- Kilometers Driven: 45,000 km
- Fuel Type: Petrol
- Transmission: Manual
- Engine: 1197 CC
- Mileage: 23.2 kmpl
- Max Power: 82 bhp
- Seats: 5
- Seller Type: Individual
- Owner: First Owner

**Expected Output:**
- Estimated Market Value: ₹4,50,000 - ₹5,50,000 (approximate range)
- Low Range: ~₹4,00,000
- Average Range: ~₹5,00,000
- High Range: ~₹6,00,000

---

## Project Structure Overview

```
AutoIntel/
├── data/                      # Dataset directory
│   └── car_details_v4.csv    # Car listings data (2,059 records)
│
├── model/                     # Trained ML models
│   ├── train_model.py        # Model training script
│   ├── car_price_model.pkl   # Best performing model
│   ├── feature_columns.pkl   # Feature encoding info
│   └── model_info.pkl        # Model metadata
│
├── app/                       # Flask web application
│   ├── app.py                # Main Flask app
│   ├── templates/            # HTML templates
│   │   ├── index.html        # Prediction form
│   │   ├── result.html       # Results page
│   │   └── about.html        # Model info
│   └── static/               # Static assets
│       ├── css/
│       │   └── style.css     # Garage-themed styling
│       ├── js/
│       │   └── script.js     # Frontend logic
│       └── images/
│           └── garage-bg.jpg # Background (optional)
│
├── requirements.txt          # Python dependencies
├── README.md                 # Full documentation
└── QUICK_START.md           # This file
```

---

## Features Included

✅ **Machine Learning Models**
- Linear Regression (Baseline)
- Random Forest Regressor
- Gradient Boosting Regressor (Best Performance)

✅ **Data Preprocessing**
- Automatic column renaming
- Missing value handling
- One-hot encoding for categorical variables
- Synthetic mileage estimation

✅ **Web Interface**
- Dark garage theme design
- Responsive layout (mobile-friendly)
- Real-time form validation
- Animated UI elements
- Professional result cards

✅ **API Endpoints**
- GET `/` - Main prediction form
- POST `/predict` - Form-based prediction
- POST `/predict_api` - JSON API
- GET `/about` - Model information

---

## Troubleshooting

### Model Training Fails
**Issue**: "KeyError: 'mileage'"  
**Solution**: The training script now auto-generates mileage estimates based on fuel type.

### Flask App Won't Start
**Issue**: "ModuleNotFoundError"  
**Solution**: 
```powershell
pip install -r requirements.txt --upgrade
```

### Port 5000 Already in Use
**Issue**: "Address already in use"  
**Solution**: Edit `app/app.py` and change the port number:
```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Predictions Seem Off
**Issue**: Unrealistic price predictions  
**Solution**: 
- Ensure all input values are realistic
- Check if the car brand is in the training dataset
- Verify numerical inputs (engine CC, mileage, max power)

---

## Model Performance

**Dataset Size**: 2,059 car listings  
**Training Set**: 1,499 records (80%)  
**Test Set**: 375 records (20%)  

### Best Model: Gradient Boosting Regressor
- **R² Score**: 0.6924 (69.24% accuracy)
- **Mean Absolute Error**: ₹5,00,899
- **Root Mean Square Error**: ₹18,97,467

### All Models Compared
| Model | Training R² | Testing R² | MAE (₹) |
|-------|------------|-----------|---------|
| Linear Regression | 0.8400 | 0.5058 | 8,60,323 |
| Random Forest | 0.9815 | 0.6687 | 5,03,267 |
| **Gradient Boosting** | **0.9682** | **0.6924** | **5,00,899** ⭐ |

---

## Customization Tips

### Change Theme Colors
Edit `app/static/css/style.css`:
```css
:root {
    --accent-orange: #ff6b35;  /* Change to your preferred color */
    --primary-dark: #1a1a1a;
    /* ... other colors */
}
```

### Add More Car Brands
Edit the brand dropdown in `app/templates/index.html`:
```html
<option value="Tesla">Tesla</option>
<option value="Porsche">Porsche</option>
```

### Adjust Price Range Calculation
Edit `app/app.py` in the `predict()` function:
```python
# Current: ±20%
low_range = predicted_price * 0.8
high_range = predicted_price * 1.2

# Wider range: ±30%
low_range = predicted_price * 0.7
high_range = predicted_price * 1.3
```

---

## Next Steps

### Immediate Actions
1. ✅ Application is running at http://127.0.0.1:5000/
2. ✅ Test with sample car data
3. ✅ Explore the About page to understand the model

### Future Enhancements
- [ ] Add more ML models (XGBoost, LightGBM)
- [ ] Include location-based pricing
- [ ] Add image upload for car photos
- [ ] Deploy to cloud (Heroku, AWS, Azure)
- [ ] Add user accounts and saved predictions
- [ ] Create price trend visualizations

---

## Support & Resources

- **Full Documentation**: See `README.md`
- **Dataset Source**: https://github.com/010Ankushsharma/datasets
- **Flask Docs**: https://flask.palletsprojects.com/
- **Scikit-learn**: https://scikit-learn.org/

---

**Enjoy predicting car prices! 🚗💨**

Built with ❤️ using Python, Machine Learning, and Flask
