import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Create directory if it doesn't exist
os.makedirs('data', exist_ok=True)

def generate_nepse_sample_data(days=180, symbol="NEPSE"):
    """Generate sample NEPSE stock data for testing."""
    # Start date (x days ago)
    start_date = datetime.now() - timedelta(days=days)
    
    # Generate dates (exclude weekends for realism)
    dates = []
    current_date = start_date
    while len(dates) < days:
        # Skip weekends (5=Saturday, 6=Sunday)
        if current_date.weekday() < 5:
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Initial price
    price = 2700.0
    
    # Lists to store data
    symbols = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []
    percent_changes = []
    
    # Previous close for percent change calculation
    prev_close = price
    
    # Generate data with some randomness but overall trend
    for i in range(len(dates)):
        # Add some seasonality and trend
        trend = 0.0001 * i  # Slight upward trend
        seasonality = 20 * np.sin(i * 0.1)  # Seasonal component
        
        # Random component for daily change (between -1% and 1%)
        daily_change = np.random.uniform(-0.01, 0.01)
        
        # Calculate price with all components
        price = price * (1 + daily_change) + trend + seasonality * 0.01
        
        # Ensure price is positive and realistic for NEPSE
        price = max(price, 1000)
        
        # Generate OHLC data
        daily_volatility = price * np.random.uniform(0.003, 0.01)
        open_price = price * (1 + np.random.uniform(-0.005, 0.005))
        high_price = max(open_price, price) + daily_volatility
        low_price = min(open_price, price) - daily_volatility
        close_price = price
        
        # Calculate percent change
        percent_change = ((close_price - prev_close) / prev_close) * 100
        
        # Update previous close for next iteration
        prev_close = close_price
        
        # Generate volume (in millions)
        volume = np.random.uniform(1000000, 10000000) * (1 + abs(percent_change) * 0.1)
        
        # Append to lists
        symbols.append(symbol)
        opens.append(round(open_price, 2))
        highs.append(round(high_price, 2))
        lows.append(round(low_price, 2))
        closes.append(round(close_price, 2))
        percent_changes.append(round(percent_change, 2))
        volumes.append(round(volume, 2))
    
    # Create DataFrame
    df = pd.DataFrame({
        'Symbol': symbols,
        'Date': dates,
        'Open': opens,
        'High': highs,
        'Low': lows,
        'Close': closes, 
        'Percent Change': percent_changes,
        'Volume': volumes
    })
    
    return df

def main():
    # Generate NEPSE Index data
    nepse_df = generate_nepse_sample_data(days=200, symbol="NEPSE")
    nepse_df.to_excel('data/NEPSE_sample.xlsx', index=False)
    print("Generated NEPSE sample data saved to data/NEPSE_sample.xlsx")
    
    # Also generate data for a few other symbols
    other_symbols = ["Banking_Index", "Finance_Index", "Hotels_Index", "Hydropower_Index"]
    
    all_data = []
    all_data.append(nepse_df)  # Add NEPSE data
    
    for symbol in other_symbols:
        # Generate with some variations
        days = np.random.randint(150, 220)
        symb_df = generate_nepse_sample_data(days=days, symbol=symbol)
        all_data.append(symb_df)
        print(f"Generated {symbol} sample data")
    
    # Combine all into one file
    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df.to_excel('data/Combined_NEPSE_sample.xlsx', index=False)
    print("Generated combined sample data saved to data/Combined_NEPSE_sample.xlsx")

if __name__ == "__main__":
    main() 