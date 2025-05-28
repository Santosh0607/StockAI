#!/usr/bin/env python3
"""
Test script for StockAI application
Tests the sample data functionality and basic app functionality
"""

import os
import sys
import pandas as pd

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.data_processor import DataProcessor
from utils.visualization import Visualizer

def test_sample_data():
    """Test if sample data can be loaded and processed"""
    print("🧪 Testing Sample Data Functionality...")
    
    # Test data files
    test_files = [
        "../testdata/CHCL_2022-02-08_2025-05-28.xlsx",
        "../testdata/HYDROPOWER_2022-02-08_2025-05-28.xlsx", 
        "../testdata/NABIL_2022-02-08_2025-05-28.xlsx",
        "../testdata/NEPSE_2022-02-08_2025-05-28.xlsx"
    ]
    
    data_processor = DataProcessor()
    visualizer = Visualizer()
    
    for file_path in test_files:
        print(f"\n📂 Testing: {os.path.basename(file_path)}")
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            continue
        
        try:
            # Load data
            df = data_processor.load_data(file_path)
            if df is None:
                print(f"❌ Failed to load data from {file_path}")
                continue
            
            # Clean data
            df_cleaned = data_processor.clean_data(df)
            if df_cleaned is None:
                print(f"❌ Failed to clean data from {file_path}")
                continue
            
            # Get dataset info
            info = data_processor.get_dataset_info(df_cleaned)
            print(f"✅ Loaded {info['total_rows']} records")
            print(f"   📅 Date range: {info['date_range']}")
            print(f"   💰 Price range: ${info['min_close']:.2f} - ${info['max_close']:.2f}")
            
            # Test visualizations
            tech_fig = visualizer.create_technical_analysis_plot(df_cleaned)
            corr_fig = visualizer.create_correlation_heatmap(df_cleaned)
            trend_fig = visualizer.create_trend_analysis_chart(df_cleaned.copy())
            
            print(f"   📊 Visualizations created successfully")
            
        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")
    
    print("\n✅ Sample data testing completed!")

def test_app_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing App Imports...")
    
    try:
        import dash
        print("✅ Dash imported successfully")
        
        import plotly.graph_objects as go
        print("✅ Plotly imported successfully")
        
        import pandas as pd
        import numpy as np
        print("✅ Data processing libraries imported successfully")
        
        from utils.data_processor import DataProcessor
        from utils.visualization import Visualizer
        print("✅ Custom modules imported successfully")
        
        # Test if model files exist
        model_files = [
            "models/lstm_model.py",
            "models/simple_lstm_model.py"
        ]
        
        for model_file in model_files:
            if os.path.exists(model_file):
                print(f"✅ {model_file} exists")
            else:
                print(f"⚠️  {model_file} not found")
        
        print("✅ All imports successful!")
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 StockAI Application Test Suite")
    print("=" * 50)
    
    # Test imports first
    if not test_app_imports():
        print("❌ Import tests failed. Please check your dependencies.")
        return
    
    print("\n" + "=" * 50)
    
    # Test sample data
    test_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\n💡 To run the application:")
    print("   python app.py")
    print("\n💡 To run the authentication app:")
    print("   python auth_app.py")

if __name__ == "__main__":
    main() 