import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import io
import base64

class Visualizer:
    def __init__(self):
        self.colors = {
            'primary': '#2D3E50',
            'secondary': '#18BC9C',
            'info': '#3498DB',
            'warning': '#F39C12',
            'danger': '#E74C3C',
            'success': '#2ECC71',
            'light': '#ECF0F1',
            'dark': '#212529'
        }
        
    def create_prediction_plot(self, dates, actual_prices, train_predict, test_predict, future_dates=None, future_prices=None):
        """
        Create an interactive plot showing actual vs predicted prices
        """
        fig = go.Figure()
        
        # Ensure data is properly flattened
        actual_prices_flat = actual_prices.flatten()
        
        # Add actual prices
        fig.add_trace(go.Scatter(
            x=dates,
            y=actual_prices_flat,
            mode='lines',
            name='Actual Prices',
            line=dict(color=self.colors['primary'], width=2)
        ))
        
        # Add training predictions
        train_plot = np.full(shape=actual_prices_flat.shape, fill_value=np.nan)
        train_predict_flat = train_predict.flatten()
        train_plot[60:60+len(train_predict_flat)] = train_predict_flat
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=train_plot,
            mode='lines',
            name='Training Predictions',
            line=dict(color=self.colors['secondary'], width=2)
        ))
        
        # Add testing predictions
        test_plot = np.full(shape=actual_prices_flat.shape, fill_value=np.nan)
        test_predict_flat = test_predict.flatten()
        test_plot[len(train_predict_flat)+60:len(train_predict_flat)+60+len(test_predict_flat)] = test_predict_flat
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=test_plot,
            mode='lines',
            name='Testing Predictions',
            line=dict(color=self.colors['warning'], width=2)
        ))
        
        # Add future predictions if available
        if future_dates is not None and future_prices is not None:
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=future_prices.flatten(),
                mode='lines',
                name='Future Predictions',
                line=dict(color=self.colors['danger'], width=2, dash='dash')
            ))
        
        # Update layout
        fig.update_layout(
            title='Stock Price Prediction',
            xaxis_title='Date',
            yaxis_title='Stock Price',
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    def create_technical_analysis_plot(self, df):
        """
        Create a technical analysis plot with candlestick and volume
        """
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, 
                            row_heights=[0.7, 0.3])
        
        # Add candlestick chart
        fig.add_trace(go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price'
        ), row=1, col=1)
        
        # Add volume bar chart if Volume column exists
        if 'Volume' in df.columns:
            fig.add_trace(go.Bar(
                x=df['Date'],
                y=df['Volume'],
                name='Volume',
                marker=dict(color=self.colors['info'])
            ), row=2, col=1)
        
        # Update layout
        fig.update_layout(
            title='Technical Analysis',
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False,
            template='plotly_white'
        )
        
        fig.update_yaxes(title_text='Volume', row=2, col=1)
        
        return fig
    
    def create_performance_metrics_chart(self, history):
        """
        Create a chart showing model training performance
        """
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            y=history.history['loss'],
            mode='lines',
            name='Training Loss',
            line=dict(color=self.colors['primary'], width=2)
        ))
        
        fig.add_trace(go.Scatter(
            y=history.history['val_loss'],
            mode='lines',
            name='Validation Loss',
            line=dict(color=self.colors['danger'], width=2)
        ))
        
        fig.update_layout(
            title='Model Training Performance',
            xaxis_title='Epoch',
            yaxis_title='Loss',
            template='plotly_white'
        )
        
        return fig
    
    def create_correlation_heatmap(self, df):
        """
        Create a correlation heatmap of the dataframe
        """
        # Select only numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
        
        # Calculate correlation matrix
        corr = numeric_df.corr()
        
        # Create heatmap
        fig = px.imshow(
            corr,
            text_auto=True,
            color_continuous_scale='RdBu_r',
            title='Correlation Heatmap'
        )
        
        fig.update_layout(
            template='plotly_white'
        )
        
        return fig
    
    def fig_to_uri(self, fig):
        """
        Convert a matplotlib figure to a base64 encoded string
        """
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return f'data:image/png;base64,{img_str}' 