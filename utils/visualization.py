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
        
        # Dark theme configuration
        self.dark_theme = {
            'plot_bgcolor': '#1a2332',
            'paper_bgcolor': '#1a2332',
            'font': {'color': '#ffffff'},
            'grid_color': 'rgba(255, 255, 255, 0.1)',
            'line_color': 'rgba(255, 255, 255, 0.2)'
        }
        
    def create_prediction_plot(self, dates, actual_prices, train_predict, test_predict, future_dates=None, future_prices=None):
        """
        Create an interactive plot showing actual vs predicted prices with dark theme
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
            line=dict(color='#ffffff', width=2.5),
            hovertemplate='<b>Actual Price</b><br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
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
            line=dict(color=self.colors['secondary'], width=2),
            hovertemplate='<b>Training Prediction</b><br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
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
            line=dict(color=self.colors['warning'], width=2),
            hovertemplate='<b>Testing Prediction</b><br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
        ))
        
        # Add future predictions if available
        if future_dates is not None and future_prices is not None:
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=future_prices.flatten(),
                mode='lines',
                name='Future Predictions',
                line=dict(color=self.colors['danger'], width=2.5, dash='dash'),
                hovertemplate='<b>Future Prediction</b><br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
            ))
        
        # Update layout with dark theme
        fig.update_layout(
            title={
                'text': 'Stock Price Prediction',
                'font': {'size': 20, 'color': '#ffffff'},
                'x': 0.5
            },
            xaxis_title='Date',
            yaxis_title='Stock Price',
            plot_bgcolor=self.dark_theme['plot_bgcolor'],
            paper_bgcolor=self.dark_theme['paper_bgcolor'],
            font=self.dark_theme['font'],
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                bgcolor='rgba(26, 35, 50, 0.8)',
                bordercolor='rgba(24, 188, 156, 0.3)',
                borderwidth=1
            ),
            xaxis=dict(
                gridcolor=self.dark_theme['grid_color'],
                linecolor=self.dark_theme['line_color'],
                zerolinecolor=self.dark_theme['line_color']
            ),
            yaxis=dict(
                gridcolor=self.dark_theme['grid_color'],
                linecolor=self.dark_theme['line_color'],
                zerolinecolor=self.dark_theme['line_color']
            )
        )
        
        return fig
    
    def create_technical_analysis_plot(self, df):
        """
        Create a technical analysis plot with candlestick and volume using dark theme
        """
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                            vertical_spacing=0.03, 
                            row_heights=[0.7, 0.3],
                            subplot_titles=('Price Chart', 'Volume'))
        
        # Add candlestick chart
        fig.add_trace(go.Candlestick(
            x=df['Date'],
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            name='Price',
            increasing_line_color='#2ECC71',
            decreasing_line_color='#E74C3C'
        ), row=1, col=1)
        
        # Add volume bar chart if Volume column exists
        if 'Volume' in df.columns:
            fig.add_trace(go.Bar(
                x=df['Date'],
                y=df['Volume'],
                name='Volume',
                marker=dict(color=self.colors['info'], opacity=0.7),
                hovertemplate='<b>Volume</b><br>Date: %{x}<br>Volume: %{y:,.0f}<extra></extra>'
            ), row=2, col=1)
        
        # Update layout with dark theme
        fig.update_layout(
            title={
                'text': 'Technical Analysis',
                'font': {'size': 20, 'color': '#ffffff'},
                'x': 0.5
            },
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False,
            plot_bgcolor=self.dark_theme['plot_bgcolor'],
            paper_bgcolor=self.dark_theme['paper_bgcolor'],
            font=self.dark_theme['font'],
            showlegend=False
        )
        
        fig.update_xaxes(
            gridcolor=self.dark_theme['grid_color'],
            linecolor=self.dark_theme['line_color'],
            zerolinecolor=self.dark_theme['line_color']
        )
        
        fig.update_yaxes(
            gridcolor=self.dark_theme['grid_color'],
            linecolor=self.dark_theme['line_color'],
            zerolinecolor=self.dark_theme['line_color']
        )
        
        fig.update_yaxes(title_text='Volume', row=2, col=1)
        
        return fig
    
    def create_performance_metrics_chart(self, history):
        """
        Create a chart showing model training performance with dark theme
        """
        fig = go.Figure()
        
        epochs = list(range(1, len(history.history['loss']) + 1))
        
        fig.add_trace(go.Scatter(
            x=epochs,
            y=history.history['loss'],
            mode='lines+markers',
            name='Training Loss',
            line=dict(color=self.colors['secondary'], width=2.5),
            marker=dict(size=6),
            hovertemplate='<b>Training Loss</b><br>Epoch: %{x}<br>Loss: %{y:.4f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=epochs,
            y=history.history['val_loss'],
            mode='lines+markers',
            name='Validation Loss',
            line=dict(color=self.colors['danger'], width=2.5),
            marker=dict(size=6),
            hovertemplate='<b>Validation Loss</b><br>Epoch: %{x}<br>Loss: %{y:.4f}<extra></extra>'
        ))
        
        # Update layout with dark theme
        fig.update_layout(
            title={
                'text': 'Model Training Performance',
                'font': {'size': 20, 'color': '#ffffff'},
                'x': 0.5
            },
            xaxis_title='Epoch',
            yaxis_title='Loss',
            plot_bgcolor=self.dark_theme['plot_bgcolor'],
            paper_bgcolor=self.dark_theme['paper_bgcolor'],
            font=self.dark_theme['font'],
            legend=dict(
                bgcolor='rgba(26, 35, 50, 0.8)',
                bordercolor='rgba(24, 188, 156, 0.3)',
                borderwidth=1
            ),
            xaxis=dict(
                gridcolor=self.dark_theme['grid_color'],
                linecolor=self.dark_theme['line_color'],
                zerolinecolor=self.dark_theme['line_color']
            ),
            yaxis=dict(
                gridcolor=self.dark_theme['grid_color'],
                linecolor=self.dark_theme['line_color'],
                zerolinecolor=self.dark_theme['line_color']
            )
        )
        
        return fig
    
    def create_correlation_heatmap(self, df):
        """
        Create a correlation heatmap of the dataframe with dark theme
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
            title='Correlation Heatmap',
            aspect='auto'
        )
        
        # Update layout with dark theme
        fig.update_layout(
            title={
                'text': 'Correlation Heatmap',
                'font': {'size': 20, 'color': '#ffffff'},
                'x': 0.5
            },
            plot_bgcolor=self.dark_theme['plot_bgcolor'],
            paper_bgcolor=self.dark_theme['paper_bgcolor'],
            font=self.dark_theme['font'],
            xaxis=dict(
                gridcolor=self.dark_theme['grid_color'],
                linecolor=self.dark_theme['line_color']
            ),
            yaxis=dict(
                gridcolor=self.dark_theme['grid_color'],
                linecolor=self.dark_theme['line_color']
            )
        )
        
        return fig
    
    def create_trend_analysis_chart(self, df):
        """
        Create a trend analysis chart with moving averages using dark theme
        """
        fig = go.Figure()
        
        # Calculate moving averages
        df['MA_7'] = df['Close'].rolling(window=7).mean()
        df['MA_21'] = df['Close'].rolling(window=21).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        
        # Add close price
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#ffffff', width=2),
            hovertemplate='<b>Close Price</b><br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
        ))
        
        # Add moving averages
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['MA_7'],
            mode='lines',
            name='7-Day MA',
            line=dict(color=self.colors['info'], width=1.5),
            hovertemplate='<b>7-Day MA</b><br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['MA_21'],
            mode='lines',
            name='21-Day MA',
            line=dict(color=self.colors['warning'], width=1.5),
            hovertemplate='<b>21-Day MA</b><br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['MA_50'],
            mode='lines',
            name='50-Day MA',
            line=dict(color=self.colors['danger'], width=1.5),
            hovertemplate='<b>50-Day MA</b><br>Date: %{x}<br>Price: %{y:.2f}<extra></extra>'
        ))
        
        # Update layout with dark theme
        fig.update_layout(
            title={
                'text': 'Trend Analysis with Moving Averages',
                'font': {'size': 20, 'color': '#ffffff'},
                'x': 0.5
            },
            xaxis_title='Date',
            yaxis_title='Price',
            plot_bgcolor=self.dark_theme['plot_bgcolor'],
            paper_bgcolor=self.dark_theme['paper_bgcolor'],
            font=self.dark_theme['font'],
            legend=dict(
                bgcolor='rgba(26, 35, 50, 0.8)',
                bordercolor='rgba(24, 188, 156, 0.3)',
                borderwidth=1
            ),
            xaxis=dict(
                gridcolor=self.dark_theme['grid_color'],
                linecolor=self.dark_theme['line_color'],
                zerolinecolor=self.dark_theme['line_color']
            ),
            yaxis=dict(
                gridcolor=self.dark_theme['grid_color'],
                linecolor=self.dark_theme['line_color'],
                zerolinecolor=self.dark_theme['line_color']
            )
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