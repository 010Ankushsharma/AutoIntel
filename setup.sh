# Quick Setup Script for AutoIntel
# Run this to get started quickly

echo "==================================="
echo "AutoIntel - Quick Setup"
echo "==================================="
echo ""

# Check Python version
echo "Checking Python version..."
python --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # For Linux/Mac
# .\venv\Scripts\Activate.ps1  # For Windows PowerShell

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download dataset (if not present)
if [ ! -f "data/car_details_v4.csv" ]; then
    echo "Downloading dataset..."
    mkdir -p data
    curl -o "data/car_details_v4.csv" "https://raw.githubusercontent.com/010Ankushsharma/datasets/refs/heads/main/car%20details%20v4.csv"
fi

# Train model (if not present)
if [ ! -f "model/car_price_model.pkl" ]; then
    echo "Training model..."
    python model/train_model.py
fi

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "To start the application:"
echo "  python app/app.py"
echo ""
echo "Then open your browser to:"
echo "  http://127.0.0.1:5000/"
echo ""
