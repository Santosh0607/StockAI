import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class DataProcessor:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
    
    def load_data(self, file_path):
        """Load data from Excel file with specific NEPSE format."""
        try:
            # Load Excel file (supports both .xlsx and .xlsm)
            df = pd.read_excel(file_path)
            
            # Check if the required columns exist
            required_columns = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                print(f"Warning: Missing required columns: {missing_columns}")
                return None
                
            # Keep only necessary columns and rename if needed
            df = df[required_columns]
            
            return df
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return None
    
    def clean_data(self, df):
        """Clean and prepare the data for analysis."""
        if df is None or df.empty:
            return None
        
        # Convert date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sort values by date
        df.sort_values(by='Date', inplace=True)
        
        # Forward fill missing values
        df.ffill(inplace=True)
        
        # Handle any potential numeric columns that might have string values
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Filter data for a single symbol if multiple symbols present
        if 'Symbol' in df.columns and len(df['Symbol'].unique()) > 1:
            # Use the most frequent symbol or NEPSE by default
            default_symbol = 'NEPSE' if 'NEPSE' in df['Symbol'].values else df['Symbol'].value_counts().idxmax()
            print(f"Multiple symbols detected. Using {default_symbol} for analysis.")
            df = df[df['Symbol'] == default_symbol].copy()
        
        # Drop Symbol column as it's not needed for time series analysis
        if 'Symbol' in df.columns:
            df = df.drop(columns=['Symbol'])
        
        # Reset index
        df.reset_index(drop=True, inplace=True)
        
        return df
    
    def prepare_for_lstm(self, df, time_step=60):
        """Prepare data for LSTM model."""
        if 'Close' not in df.columns:
            raise KeyError("'Close' column is missing in the DataFrame.")
        
        # Ensure Close is float
        df['Close'] = df['Close'].astype(float)
        
        # Get Close prices
        prices = df['Close'].values.reshape(-1, 1)
        
        # Scale prices
        scaled_prices = self.scaler.fit_transform(prices)
        
        # Create dataset with time steps
        X, y = self._create_dataset(scaled_prices, time_step)
        
        # Reshape for LSTM [samples, time steps, features]
        X = X.reshape(X.shape[0], X.shape[1], 1)
        
        # Split into train and test sets
        train_size = int(len(X) * 0.8)
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]
        
        return X_train, X_test, y_train, y_test, prices
    
    def _create_dataset(self, dataset, time_step=1):
        """Create a dataset with time steps."""
        X, y = [], []
        for i in range(len(dataset) - time_step):
            X.append(dataset[i:(i + time_step), 0])
            y.append(dataset[i + time_step, 0])
        return np.array(X), np.array(y)
    
    def prepare_for_prediction(self, df, time_step=60):
        """Prepare the last time_step days of data for prediction."""
        df['Close'] = df['Close'].astype(float)
        last_data = df['Close'].values[-time_step:].reshape(-1, 1)
        last_data_scaled = self.scaler.transform(last_data)
        X = last_data_scaled.reshape(1, time_step, 1)
        return X
    
    def inverse_transform(self, data):
        """Inverse transform scaled data."""
        return self.scaler.inverse_transform(data)
        
    def get_dataset_info(self, df):
        """Get basic information about the dataset for display."""
        if df is None or df.empty:
            return None
            
        info = {
            "total_rows": len(df),
            "date_range": f"{df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}",
            "min_close": df['Close'].min(),
            "max_close": df['Close'].max(),
            "avg_close": df['Close'].mean(),
            "avg_volume": df['Volume'].mean(),
            "columns": list(df.columns)
        }
        
        return info 