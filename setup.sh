#!/bin/bash
# Gen AI Content Transformer - Setup Script
# Sets up the virtual environment and installs dependencies

set -e

echo "========================================="
echo " Gen AI Content Transformer - Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate
source .venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .streamlit config
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[server]
headless = true
address = "0.0.0.0"
port = 8501

[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false
EOF

echo ""
echo "========================================="
echo " Setup Complete!"
echo "========================================="
echo ""
echo "To run the application:"
echo ""
echo "  source .venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "The app will open at http://localhost:8501"
echo ""
echo "NOTE: On first run, TinyLlama (~2GB) will be"
echo "      downloaded automatically and cached locally."
echo ""
