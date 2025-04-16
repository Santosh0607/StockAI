# Stocks AI - NEPSE Market Prediction

A machine learning application for predicting stock market trends using LSTM and SimpleRNN models.

## Features

- Upload and process stock market data in Excel format
- Clean and preprocess time series data automatically
- Train deep learning models on historical data
- Visualize predictions with interactive charts
- Technical analysis and correlation heatmaps
- Future price prediction for up to 90 days

## Getting Started

### Prerequisites

- Python 3.8+ installed
- Required packages (see `requirements.txt`)

### Installation

1. Clone the repository or download the source code
2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python app.py
```
or use the provided batch file:
```
run_app.bat
```

4. The application will be available at http://127.0.0.1:8050/ in your web browser

## Usage Guide

1. **Upload Data**: Click the upload box to select an Excel file or drag and drop. The file should contain stock data with columns: Symbol, Date, Open, High, Low, Close, and Volume.

2. **Configure Model Parameters**:
   - **Time Step (Days to Look Back)**: The number of previous days used to predict the next day's price (default: 60)
   - **Prediction Days**: How many days into the future to predict (default: 30)
   - **Training Ratio**: Percentage of data used for training (default: 0.8)
   - **Model Type**: Choose between:
     - **LSTM (Complex)**: More accurate but may have compatibility issues
     - **SimpleRNN (Compatible)**: Simpler model with better compatibility

3. **Train Model & Predict**: Click the button to process the data and generate predictions

4. **Analyze Results**: View the generated charts and metrics:
   - **Price Prediction**: Historical data and future predictions
   - **Technical Analysis**: Key indicators like moving averages
   - **Model Performance**: Training and validation metrics
   - **Correlation Analysis**: Relationships between different features
   - **Trend Analysis**: Short-term trend visualization

## Data Format

Your Excel file should follow this format:

| Symbol | Date       | Open    | High    | Low     | Close   | Volume        |
|--------|------------|---------|---------|---------|---------|---------------|
| NEPSE  | 2025-04-12 | 2677.58 | 2687.92 | 2667.00 | 2670.77 | 5,637,981,250 |

## Model Information

### LSTM (Long Short-Term Memory)
- Complex architecture for capturing long-term dependencies
- Better for larger datasets with clear patterns
- More computationally intensive

### SimpleRNN
- Simplified recurrent neural network architecture
- More compatible with different environments
- Faster training with comparable results for many datasets
- Automatically used as fallback if LSTM fails

## Troubleshooting

- **Model Training Errors**: Try using the SimpleRNN model type
- **Data Format Issues**: Ensure your Excel file follows the required format
- **Dependency Errors**: Check that all packages in requirements.txt are installed

## License

This project is open source and available under the MIT License.

## Acknowledgments

- The NEPSE (Nepal Stock Exchange) for data inspiration
- TensorFlow and Keras for machine learning capabilities
- Dash and Plotly for interactive visualizations 