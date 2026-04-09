# AutoIntel - Car Price Prediction System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.0](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚗 AI-Powered Car Price Prediction

A production-ready machine learning web application that predicts car resale values using advanced Gradient Boosting algorithms. Features a premium high-tech UI with real-time predictions and comprehensive market analysis.

![AutoIntel Preview](preview.png)

**Live Demo**:https://autointel.onrender.com

---

## ✨ Features

### 🔮 Machine Learning
- **Gradient Boosting Model** with 69.24% R² accuracy
- **Multi-Model Training**: Linear Regression, Random Forest, Gradient Boosting
- **Automated Feature Engineering**: One-hot encoding, data preprocessing
- **Real-time Predictions**: Instant price estimates with market ranges

### 🎨 Premium UI/UX
- **High-Tech Theme**: Greyish premium design with neon cyan accents
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Advanced Animations**: Smooth transitions and hover effects
- **Professional Branding**: Creator showcase and contact integration

### 🛠️ Production Ready
- **Error Handling**: Comprehensive validation and error messages
- **Model Serialization**: Joblib-pickled models for fast loading
- **RESTful API**: JSON endpoints for programmatic access
- **Deployment Ready**: Docker, Heroku, AWS compatible

---

## 📋 Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Model Performance](#model-performance)
- [Deployment](#deployment)
- [Technologies](#technologies)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/010Ankushsharma/AutoIntel.git
cd AutoIntel
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Download Dataset
The dataset is available at:
```
https://raw.githubusercontent.com/010Ankushsharma/datasets/refs/heads/main/car%20details%20v4.csv
```

Place it in `data/car_details_v4.csv`

### Step 5: Train Model
```bash
python model/train_model.py
```

This will:
- Load and preprocess the dataset
- Train three ML models
- Select the best performer (Gradient Boosting)
- Save models to `model/` directory

---

## 💻 Usage

### Start Flask Server
```bash
python app/app.py
```

### Access Application
Open your browser to:
```
http://127.0.0.1:5000/
```

### Make a Prediction
1. Navigate to the prediction form
2. Enter car specifications:
   - Manufacturer (Brand)
   - Model Year
   - Kilometers Driven
   - Fuel Type
   - Transmission
   - Engine Capacity
   - Mileage
   - Max Power
   - Seating Capacity
   - Seller Type
   - Ownership History
3. Click "Calculate Value"
4. View instant AI-powered valuation with market ranges

---

## 📁 Project Structure

```
AutoIntel/
│
├── .github/                    # GitHub configuration
│   └── workflows/
│       └── deploy.yml         # CI/CD pipeline
│
├── data/                       # Dataset directory
│   └── car_details_v4.csv     # Car listings (not included in repo)
│
├── model/                      # Trained ML models
│   ├── train_model.py         # Model training script
│   ├── car_price_model.pkl    # Best performing model
│   ├── feature_columns.pkl    # Feature mappings
│   └── model_info.pkl         # Model metadata
│
├── app/                        # Flask web application
│   ├── app.py                 # Main Flask application
│   │
│   ├── templates/             # HTML templates
│   │   ├── index-premium.html # Homepage with prediction form
│   │   └── result-premium.html # Results display
│   │
│   └── static/                # Static assets
│       ├── css/
│       │   └── style-premium.css  # Premium theme
│       ├── js/
│       │   └── script.js      # Frontend logic
│       └── images/
│           └── hero-car-premium.jpg (optional)
│
├── .gitignore                 # Git ignore rules
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python version for deployment
├── Procfile                  # Deployment entry point
├── README.md                 # This file
└── LICENSE                   # MIT License
```

---

## 🔌 API Endpoints

### GET `/`
Renders the main prediction page.

**Response**: HTML page

---

### POST `/predict`
Processes form submission and returns prediction results.

**Request**: Form data (application/x-www-form-urlencoded)
```
year=2020&km_driven=50000&fuel=Petrol&transmission=Manual&
owner=First_Owner&brand=Maruti Suzuki&engine=1200&
mileage=15.0&max_power=80.0&seats=5
```

**Response**: HTML result page with predicted price

---

### POST `/predict_api`
JSON API for programmatic access.

**Request**: JSON
```json
{
  "year": 2020,
  "km_driven": 50000,
  "fuel": "Petrol",
  "seller_type": "Individual",
  "transmission": "Manual",
  "owner": "First_Owner",
  "brand": "Maruti Suzuki",
  "engine": 1200,
  "mileage": 15.0,
  "max_power": 80.0,
  "seats": 5
}
```

**Response**: JSON
```json
{
  "predicted_price": 586552.71,
  "currency": "INR",
  "low_range": 469242.17,
  "high_range": 703863.25,
  "success": true,
  "message": "Prediction successful"
}
```

---

## 📊 Model Performance

### Dataset Statistics
- **Total Records**: 2,059 car listings
- **Training Set**: 1,647 records (80%)
- **Test Set**: 412 records (20%)
- **Features After Encoding**: 49 columns

### Model Comparison

| Model | Training R² | Testing R² | MAE (₹) | RMSE (₹) |
|-------|------------|-----------|---------|----------|
| Linear Regression | 0.8400 | 0.5058 | 860,323 | 2,405,233 |
| Random Forest | 0.9815 | 0.6687 | 503,267 | 1,969,465 |
| **Gradient Boosting** | **0.9682** | **0.6924** | **500,899** | **1,897,467** |

### Best Model: Gradient Boosting Regressor
- **R² Score**: 0.6924 (69.24% accuracy)
- **Mean Absolute Error**: ₹500,899
- **Root Mean Square Error**: ₹1,897,467

---

## 🌐 Deployment

### Deploy to Heroku

1. **Install Heroku CLI**
```bash
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
heroku create autointel-car-prediction
```

4. **Initialize Git** (if not already done)
```bash
git init
git add .
git commit -m "Initial commit"
```

5. **Add Heroku Remote**
```bash
heroku git:remote -a autointel-car-prediction
```

6. **Deploy**
```bash
git push heroku main
```

7. **Open App**
```bash
heroku open
```

### Deploy to Railway

1. Visit [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variables (if needed)
4. Deploy automatically on push

### Deploy with Docker

1. **Build Docker Image**
```bash
docker build -t autointel .
```

2. **Run Container**
```bash
docker run -p 5000:5000 autointel
```

3. **Push to Registry**
```bash
docker tag autointel username/autointel:latest
docker push username/autointel:latest
```

---

## 🛠️ Technologies

### Backend
- **Python 3.8+**: Core programming language
- **Flask 3.0**: Web framework
- **Pandas 2.1**: Data manipulation
- **NumPy 1.26**: Numerical computing
- **Scikit-Learn 1.3**: Machine learning
- **Joblib 1.3**: Model serialization

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Advanced styling with gradients, animations
- **JavaScript ES6+**: Interactive functionality
- **Google Fonts**: Orbitron, Roboto

### Machine Learning
- **Gradient Boosting Regressor**: Primary model
- **Random Forest Regressor**: Ensemble method
- **Linear Regression**: Baseline model
- **One-Hot Encoding**: Categorical features
- **Train-Test Split**: 80/20 partitioning

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
1. Check existing issues
2. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected behavior
   - Screenshots (if applicable)

### Suggesting Features
1. Open an issue with feature proposal
2. Explain use case and benefits
3. Discuss implementation approach

### Pull Requests
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Comment complex logic

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Summary**: Free to use, modify, and distribute with attribution.

---

## 👨‍💻 Contact

### Created By
**Ankush Sharma**  
Developer & Data Scientist

- 📱 **Phone**: +91 7814790285
- 💼 **LinkedIn**: [linkedin.com/in/ankush-sharma-b63a5624a/](https://www.linkedin.com/in/ankush-sharma-b63a5624a/)
- 🐙 **GitHub**: [github.com/010Ankushsharma](https://github.com/010Ankushsharma)

### Project Links
- **Repository**: [github.com/010Ankushsharma/AutoIntel](https://github.com/010Ankushsharma/AutoIntel)
- **Report Issue**: [GitHub Issues](https://github.com/010Ankushsharma/AutoIntel/issues)

---

## 📈 Future Enhancements

- [ ] Add XGBoost and LightGBM models
- [ ] Implement location-based pricing
- [ ] Add image recognition for car photos
- [ ] Create user accounts and saved predictions
- [ ] Build price trend visualizations
- [ ] Add multi-language support
- [ ] Deploy to cloud platform
- [ ] Integrate real-time market data API

---

## 🙏 Acknowledgments

- Dataset: [010Ankushsharma/datasets](https://github.com/010Ankushsharma/datasets)
- Scikit-Learn documentation
- Flask community
- Modern web technologies

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/010Ankushsharma/AutoIntel?style=social)
![GitHub forks](https://img.shields.io/github/forks/010Ankushsharma/AutoIntel?style=social)
![GitHub issues](https://img.shields.io/github/issues/010Ankushsharma/AutoIntel)
![GitHub license](https://img.shields.io/github/license/010Ankushsharma/AutoIntel)

---

**Made with ❤️ by Ankush Sharma**  
*Powered by Advanced Machine Learning & Modern Web Technologies*
