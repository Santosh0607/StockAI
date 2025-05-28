# 🚀 StockAI - NEPSE Market Prediction

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Dash](https://img.shields.io/badge/Dash-2.0+-green.svg)](https://dash.plotly.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An advanced AI-powered stock market prediction application for the Nepal Stock Exchange (NEPSE) with a beautiful dark-themed interface and comprehensive analytics.

## ✨ New Features & Fixes

### 🔧 Recent Updates
- **Fixed Authentication UI**: Login/signup buttons now have proper positioning and beautiful styling
- **Dark Chart Themes**: All charts now use elegant dark backgrounds instead of painful white colors
- **Test Sample Data**: Beautiful new feature with 4 curated sample datasets for testing
- **Enhanced Visualizations**: Improved chart styling with better hover effects and dark theme
- **Better Button Design**: Fixed button positioning and added smooth animations

### 🧪 Test Sample Data
The app now includes 4 professionally curated sample datasets:

- **CHCL** - Chilime Hydropower Limited (Energy/Hydropower)
- **HYDROPOWER** - Hydropower Sector Index (Energy/Hydropower)
- **NABIL** - Nabil Bank Limited (Banking)
- **NEPSE** - NEPSE Index (Market Index)

Simply click the beautiful "Test Sample DATA" button to explore these datasets!

## 🎯 Features

### 📊 Advanced Analytics
- **LSTM & SimpleRNN Models** - Choose between complex LSTM or compatible SimpleRNN models
- **Real-time Predictions** - AI-powered future price predictions
- **Technical Analysis** - Candlestick charts with volume analysis
- **Correlation Analysis** - Heatmaps showing market correlations
- **Trend Analysis** - Moving averages and trend indicators

### 🎨 Beautiful UI
- **Dark Glassmorphic Design** - Modern, eye-friendly interface
- **Responsive Layout** - Works perfectly on all devices
- **Interactive Charts** - Plotly-powered visualizations with dark themes
- **Smooth Animations** - Elegant transitions and hover effects

### 🔐 Secure Authentication
- **User Registration** - Secure account creation
- **Session Management** - Safe user sessions
- **Password Security** - Bcrypt password hashing

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
cd StockAI

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Start the authentication server (Terminal 1)
python auth_app.py

# Start the main application (Terminal 2)
python app.py
```

### 3. Access the Application
- **Main App**: http://127.0.0.1:8050
- **Authentication**: http://127.0.0.1:8060

### 4. Test the App
```bash
# Run the test suite
python test_app.py
```

## 📁 Project Structure

```
StockAI/
├── app.py                 # Main Dash application
├── auth_app.py           # Authentication application
├── auth.py               # Authentication backend
├── test_app.py           # Test suite
├── requirements.txt      # Python dependencies
├── stockai_users.db      # User database
├── assets/
│   └── style.css         # Enhanced dark theme styles
├── utils/
│   ├── data_processor.py # Data processing utilities
│   └── visualization.py # Chart generation with dark themes
├── models/
│   ├── lstm_model.py     # LSTM model implementation
│   └── simple_lstm_model.py # SimpleRNN model implementation
└── data/                 # Data storage directory
```

## 🎮 How to Use

### 📤 Upload Data
1. **Drag & Drop**: Simply drag your Excel file to the upload area
2. **Test Sample Data**: Click the "Test Sample DATA" button for instant testing
3. **Required Format**: Excel files with columns: Symbol, Date, Open, High, Low, Close, Volume

### 🤖 Train Models
1. **Choose Parameters**: Adjust time steps, prediction days, and training ratio
2. **Select Model**: Choose between LSTM Complex or SimpleRNN Compatible
3. **Train & Predict**: Click "Train Model & Predict" to start analysis

### 📈 Analyze Results
- **Price Predictions**: View actual vs predicted prices with future forecasts
- **Technical Analysis**: Examine candlestick charts and volume patterns
- **Model Performance**: Monitor training and validation metrics
- **Correlation Analysis**: Understand market relationships

## 🛠️ Configuration

### Sample Data Location
The app expects sample data files in `../testdata/` directory with these files:
- `CHCL_2022-02-08_2025-05-28.xlsx`
- `HYDROPOWER_2022-02-08_2025-05-28.xlsx`
- `NABIL_2022-02-08_2025-05-28.xlsx`
- `NEPSE_2022-02-08_2025-05-28.xlsx`

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here  # Optional: for session security
```

## 🎨 UI Improvements

### Dark Theme Features
- **Chart Backgrounds**: All charts now use `#1a2332` dark background
- **Grid Lines**: Subtle white grid lines with 10% opacity
- **Text Colors**: White text with proper contrast ratios
- **Button Styling**: Enhanced buttons with hover animations
- **Modal Design**: Beautiful sample data selection modal

### Responsive Design
- **Mobile Friendly**: Works perfectly on mobile devices
- **Tablet Support**: Optimized for tablet viewing
- **Desktop Enhanced**: Full-featured desktop experience

## 🧪 Sample Data Testing

The app includes a comprehensive test suite:

```bash
python test_app.py
```

This will test:
- ✅ All required imports
- ✅ Sample data loading
- ✅ Data processing pipeline
- ✅ Visualization generation
- ✅ Model file availability

## 📊 Supported Data Formats

### Excel Requirements
Your Excel file should contain these columns:
- **Symbol**: Stock symbol (e.g., "NEPSE", "NABIL")
- **Date**: Trading date in any standard format
- **Open**: Opening price
- **High**: Highest price of the day
- **Low**: Lowest price of the day
- **Close**: Closing price
- **Volume**: Trading volume

### Example Data Format
| Symbol | Date       | Open    | High    | Low     | Close   | Volume        |
|--------|------------|---------|---------|---------|---------|---------------|
| NEPSE  | 2025-04-12 | 2677.58 | 2687.92 | 2667.00 | 2670.77 | 5,637,981,250 |

## 🔧 Technical Details

### AI Models
- **LSTM (Long Short-Term Memory)**: Advanced model for complex patterns
- **SimpleRNN**: Compatible model for broader system support
- **Automatic Fallback**: System automatically uses SimpleRNN if LSTM fails

### Performance Metrics
- **Training Accuracy**: RMSE-based accuracy for training data
- **Testing Accuracy**: RMSE-based accuracy for test data
- **Prediction Trend**: Bullish/Bearish/Neutral trend indication
- **Future Change**: Percentage change prediction

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NEPSE** - Nepal Stock Exchange for market data structure
- **Plotly** - For beautiful, interactive charts
- **Dash** - For the modern web application framework
- **TensorFlow/Keras** - For AI model implementation

---

**Happy Trading! 📈✨**

*Built with ❤️ for the NEPSE trading community* 