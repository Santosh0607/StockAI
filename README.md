# 🚀 StockAI - NEPSE Market Prediction Platform

A modern, secure web application for predicting NEPSE (Nepal Stock Exchange) market trends using AI/ML models with a beautiful glassmorphic dark theme UI.

## ✨ Features

### 🔐 **Secure Authentication System**
- User registration and login
- Password hashing with PBKDF2-SHA256
- Session management with 24-hour timeout
- SQLite database with encrypted storage
- Input validation and security features

### 📊 **AI-Powered Stock Prediction**
- LSTM and SimpleRNN models for stock price prediction
- Technical analysis indicators
- Interactive charts and visualizations
- Model performance metrics
- Future price predictions

### 🎨 **Modern UI/UX**
- Glassmorphic dark theme design
- Responsive design (desktop, tablet, mobile)
- Smooth animations and transitions
- Neon accent colors (blue/green theme)
- Professional fintech aesthetic

### 📈 **Data Analysis Features**
- Excel file upload support
- Data validation and cleaning
- Statistical analysis
- Correlation heatmaps
- Multiple visualization tabs

## 🛡️ **Security Implementation**

### Database Security
- **Database**: SQLite with SQLAlchemy ORM
- **Password Storage**: PBKDF2-SHA256 hashing with 16-byte salt
- **SQL Injection Protection**: Parameterized queries
- **Session Security**: Secure tokens with automatic cleanup

### Authentication Features
- Email validation and sanitization
- Password strength requirements:
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 lowercase letter
  - At least 1 number
- User account status tracking
- Login attempt monitoring

### Session Management
- 24-hour session timeout
- Secure session tokens (32-byte hex)
- CSRF protection tokens
- Automatic session cleanup

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd StockAI-master
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run_stockai.py
   ```

4. **Access the applications**
   - 🔑 **Authentication**: http://127.0.0.1:8060
   - 📈 **Main Dashboard**: http://127.0.0.1:8050

### Alternative: Run Components Separately

**Start Authentication System:**
```bash
python auth_app.py
```

**Start Main Dashboard:**
```bash
python app.py
```

## 📋 **How to Use**

### Step 1: Create Account / Login
1. Open the authentication page (http://127.0.0.1:8060)
2. Click "Sign Up" to create a new account or use "Login" for existing accounts
3. Fill in your details with a strong password
4. After successful login, you'll get a link to the main dashboard

### Step 2: Upload Stock Data
1. Access the main dashboard (http://127.0.0.1:8050)
2. Upload an Excel file (.xlsx) with the following columns:
   - **Symbol**: Stock symbol (e.g., NEPSE)
   - **Date**: Trading date
   - **Open**: Opening price
   - **High**: Highest price
   - **Low**: Lowest price
   - **Close**: Closing price
   - **Volume**: Trading volume

### Step 3: Configure Model Parameters
1. Set time step (recommended: 60)
2. Set prediction days (recommended: 30)
3. Set training ratio (recommended: 0.8)
4. Choose model type (LSTM Complex or SimpleRNN Compatible)

### Step 4: Train Model and View Results
1. Click "Train Model & Predict"
2. Wait for training to complete
3. View results in multiple tabs:
   - **Price Prediction**: Future price forecasts
   - **Technical Analysis**: Technical indicators
   - **Model Performance**: Training metrics
   - **Correlation Analysis**: Data correlations

## 📊 **Data Format Example**

| Symbol | Date       | Open    | High    | Low     | Close   | Volume          |
|--------|------------|---------|---------|---------|---------|-----------------|
| NEPSE  | 2025-04-12 | 2677.58 | 2687.92 | 2667.00 | 2670.77 | 5,637,981,250.23|
| NEPSE  | 2025-04-11 | 2665.23 | 2678.45 | 2660.12 | 2675.89 | 4,892,543,123.45|

## 🔧 **Configuration**

### Environment Variables
- `SECRET_KEY`: Flask secret key for session encryption (auto-generated if not set)

### Database Location
- SQLite database: `stockai_users.db` (created automatically)

### Ports
- Authentication System: 8060
- Main Dashboard: 8050

## 🏗️ **Architecture**

```
StockAI/
├── auth.py              # Authentication system core
├── auth_app.py          # Authentication web application
├── app.py               # Main dashboard application
├── run_stockai.py       # Application runner
├── requirements.txt     # Python dependencies
├── assets/
│   └── style.css       # Modern glassmorphic CSS
├── models/             # AI/ML models
├── utils/              # Data processing utilities
└── output/             # Generated files
```

## 🛠️ **Dependencies**

- **Web Framework**: Dash, Flask
- **Database**: SQLAlchemy, SQLite
- **Security**: Flask-Login, Flask-Bcrypt, Werkzeug
- **AI/ML**: TensorFlow, scikit-learn
- **Data**: Pandas, NumPy
- **Visualization**: Plotly
- **UI**: Dash Bootstrap Components

## 🔒 **Production Deployment Recommendations**

For production use, consider these enhancements:

1. **Database**: Switch to PostgreSQL or MySQL
2. **SSL/TLS**: Enable HTTPS encryption
3. **Rate Limiting**: Implement login attempt limits
4. **Email Verification**: Add email confirmation
5. **Monitoring**: Set up logging and monitoring
6. **Backups**: Regular database backups
7. **Environment**: Use environment variables for sensitive data

## 🐛 **Troubleshooting**

### Common Issues

**Port Already in Use:**
- The runner script will detect and offer to kill existing processes
- Manually kill processes: `lsof -ti:8050 | xargs kill -9`

**Database Issues:**
- Delete `stockai_users.db` to reset the database
- Check file permissions

**Import Errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.8 or higher

**Authentication Issues:**
- Clear browser cookies and sessions
- Check that both applications are running

## 📝 **License**

This project is for educational and research purposes. Please ensure compliance with local regulations when used with real financial data.

## 🤝 **Contributing**

Feel free to fork, modify, and enhance this project. Areas for improvement:
- Additional ML models
- More technical indicators
- Enhanced security features
- Real-time data integration
- Mobile app version

## 📞 **Support**

For issues or questions:
1. Check the troubleshooting section
2. Review console logs for errors
3. Ensure all dependencies are properly installed

---

**🎯 Built with modern web technologies and security best practices for NEPSE market analysis.** 