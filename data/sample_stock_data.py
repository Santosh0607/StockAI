import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Create directory if it doesn't exist
os.makedirs('data', exist_ok=True)

# Function to generate sample stock data
def generate_sample_stock_data(days=500):
    """Generate sample stock data for testing."""
    # Start date (500 days ago)
    start_date = datetime.now() - timedelta(days=days)
    
    # Generate dates
    dates = [start_date + timedelta(days=i) for i in range(days)]
    
    # Initial price
    price = 1000.0
    
    # Lists to store data
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []
    
    # Generate data with some randomness but overall trend
    for i in range(days):
        # Add some seasonality and trend
        trend = 0.0002 * i  # Slight upward trend
        seasonality = 50 * np.sin(i * 0.1)  # Seasonal component
        
        # Random component for daily change (between -2% and 2%)
        daily_change = np.random.uniform(-0.02, 0.02)
        
        # Calculate price with all components
        price = price * (1 + daily_change) + trend + seasonality * 0.01
        
        # Ensure price is positive
        price = max(price, 100)
        
        # Generate OHLC data
        daily_volatility = price * np.random.uniform(0.005, 0.02)
        open_price = price * (1 + np.random.uniform(-0.01, 0.01))
        high_price = max(open_price, price) + daily_volatility
        low_price = min(open_price, price) - daily_volatility
        close_price = price
        
        # Generate volume (in thousands)
        volume = np.random.randint(50, 5000)
        
        # Append to lists
        opens.append(open_price)
        highs.append(high_price)
        lows.append(low_price)
        closes.append(close_price)
        volumes.append(volume)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Open': opens,
        'High': highs,
        'Low': lows,
        'Close': closes,
        'Volume': volumes
    })
    
    return df

# Generate and save sample stock data
sample_df = generate_sample_stock_data()
sample_df.to_excel('data/sample_stock_data.xlsx', index=False)

print("Sample stock data generated and saved to data/sample_stock_data.xlsx")

# Generate and save multiple stock indices
indices = [
    "NEPSE_Index",
    "Banking_Index",
    "Finance_Index",
    "Microfinance_Index",
    "Insurance_Index",
    "Hydropower_Index"
]

for index_name in indices:
    # Generate with some variations
    days = np.random.randint(400, 600)
    sample_df = generate_sample_stock_data(days)
    
    # Save to file
    file_path = f"data/{index_name}.xlsx"
    sample_df.to_excel(file_path, index=False)
    print(f"Sample data for {index_name} saved to {file_path}")

print("All sample files generated!")