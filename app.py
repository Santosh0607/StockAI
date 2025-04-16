import os
import datetime
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

# Import custom modules
from utils.data_processor import DataProcessor
from models.lstm_model import LSTMModel
from models.simple_lstm_model import SimpleLSTMModel  # Import the simple model as fallback
from utils.visualization import Visualizer

# Initialize data processor, model, and visualizer
data_processor = DataProcessor()
visualizer = Visualizer()

# Create output directory if it doesn't exist
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Stocks AI - NEPSE Market Prediction"
server = app.server

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        dbc.Container([
            html.H1([
                "Stocks ", html.Span("AI", style={"color": "#18BC9C"}),
                " - NEPSE Market Prediction"
            ], className="header-title")
        ])
    ], className="app-header mb-4"),
    
    # Main content
    dbc.Container([
        # File upload section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Upload Stock Data"),
                    dbc.CardBody([
                        html.Div([
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    html.Div(className="upload-box-icon", children="📈"),
                                    html.Div('Drag and Drop or Click to Select Files'),
                                    html.Div('Accept Excel (.xlsx, .xlsm) files', 
                                             style={"fontSize": "0.8rem", "opacity": "0.7"})
                                ]),
                                style={},
                                multiple=False,
                                className="upload-box"
                            )
                        ]),
                        html.Div(id='upload-output', className="mt-3"),
                        
                        # Expected format helper
                        html.Div([
                            html.H6("Expected Data Format:", className="mt-3"),
                            html.P("Your Excel file should include these columns:"),
                            dbc.Table([
                                html.Thead(
                                    html.Tr([
                                        html.Th("Symbol"), html.Th("Date"), html.Th("Open"), 
                                        html.Th("High"), html.Th("Low"), html.Th("Close"), 
                                        html.Th("Volume")
                                    ])
                                ),
                                html.Tbody([
                                    html.Tr([
                                        html.Td("NEPSE"), html.Td("2025-04-12"), html.Td("2677.58"), 
                                        html.Td("2687.92"), html.Td("2667.00"), html.Td("2670.77"), 
                                        html.Td("5,637,981,250.23")
                                    ])
                                ])
                            ], bordered=True, size="sm", className="mt-2")
                        ], id="format-helper", className="mt-3"),
                        
                        # Model parameters section
                        html.Div([
                            html.H5("Model Parameters", className="mt-4 mb-3"),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Time Step (Days to Look Back)"),
                                    dbc.Input(id="time-step", type="number", value=60, min=1, max=200)
                                ], md=6),
                                dbc.Col([
                                    html.Label("Prediction Days"),
                                    dbc.Input(id="prediction-days", type="number", value=30, min=1, max=90)
                                ], md=6)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Label("Training Ratio"),
                                    dbc.Input(id="train-ratio", type="number", value=0.8, min=0.5, max=0.9, step=0.05)
                                ], md=6),
                                dbc.Col([
                                    html.Label("Model Type"),
                                    dbc.Select(
                                        id="model-type",
                                        options=[
                                            {"label": "LSTM (Complex)", "value": "lstm"},
                                            {"label": "SimpleRNN (Compatible)", "value": "simple"}
                                        ],
                                        value="simple"
                                    )
                                ], md=6)
                            ], className="mt-3")
                        ], id="model-params-container", style={"display": "none"}),
                        
                        # Train button
                        html.Div([
                            dbc.Button("Train Model & Predict", 
                                      id="train-button", 
                                      color="secondary", 
                                      className="mt-3",
                                      disabled=True)
                        ])
                    ])
                ])
            ], md=4),
            
            # Data preview section
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Data Preview"),
                    dbc.CardBody([
                        dcc.Loading(
                            id="loading-data-preview",
                            type="default",
                            children=[
                                html.Div(id="data-preview-container")
                            ]
                        )
                    ])
                ])
            ], md=8)
        ]),
        
        # Model training and prediction section (appears after training)
        html.Div([
            dbc.Row([
                # Stats cards
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div(html.H4(id="training-accuracy", children="0%"), 
                                         className="stats-card-value"),
                                html.Div("Training Accuracy", className="stats-card-title")
                            ], className="stats-card info")
                        ], md=6),
                        dbc.Col([
                            html.Div([
                                html.Div(html.H4(id="testing-accuracy", children="0%"), 
                                         className="stats-card-value"),
                                html.Div("Testing Accuracy", className="stats-card-title")
                            ], className="stats-card warning")
                        ], md=6)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Div(html.H4(id="prediction-trend", children="-"), 
                                         className="stats-card-value"),
                                html.Div("Predicted Trend", className="stats-card-title")
                            ], className="stats-card secondary")
                        ], md=6),
                        dbc.Col([
                            html.Div([
                                html.Div(html.H4(id="future-change", children="0%"), 
                                         className="stats-card-value"),
                                html.Div("Predicted Change", className="stats-card-title")
                            ], className="stats-card primary")
                        ], md=6)
                    ])
                ], md=4),
                
                # Trend analysis
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Trend Analysis"),
                        dbc.CardBody([
                            dcc.Graph(id="trend-analysis-chart")
                        ])
                    ])
                ], md=8)
            ], className="mt-4"),
            
            # Visualization tabs
            dbc.Card([
                dbc.CardHeader("Visualizations"),
                dbc.CardBody([
                    # Tabs for different visualizations
                    dbc.Tabs([
                        dbc.Tab([
                            dcc.Graph(id="prediction-chart")
                        ], label="Price Prediction"),
                        dbc.Tab([
                            dcc.Graph(id="technical-chart")
                        ], label="Technical Analysis"),
                        dbc.Tab([
                            dcc.Graph(id="performance-chart")
                        ], label="Model Performance"),
                        dbc.Tab([
                            dcc.Graph(id="correlation-chart")
                        ], label="Correlation Analysis")
                    ])
                ])
            ], className="mt-4")
        ], id="results-container", style={"display": "none"}),
        
        # Footer
        html.Footer([
            html.P(["Stocks AI - NEPSE Market Prediction © ", 
                   str(datetime.datetime.now().year)]),
            html.P(["Built with ", 
                   html.A("Dash", href="https://dash.plotly.com/", target="_blank"),
                   " and ",
                   html.A("TensorFlow", href="https://www.tensorflow.org/", target="_blank")])
        ], className="footer")
    ])
])

# Global variables to store data and model
current_data = None
trained_model = None
model_history = None
training_predictions = None
testing_predictions = None
future_predictions = None

# Callback for file upload
@app.callback(
    [Output("upload-output", "children"),
     Output("data-preview-container", "children"),
     Output("model-params-container", "style"),
     Output("train-button", "disabled")],
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")]
)
def update_output(contents, filename):
    global current_data
    
    if contents is None:
        return (
            "",
            html.Div("No data uploaded yet."),
            {"display": "none"},
            True
        )
    
    # Check file extension
    if not (filename.endswith('.xlsx') or filename.endswith('.xlsm')):
        return (
            html.Div("Please upload an Excel (.xlsx or .xlsm) file.", className="text-danger"),
            html.Div("Invalid file format."),
            {"display": "none"},
            True
        )
    
    # Save the uploaded file
    content_type, content_string = contents.split(',')
    import base64
    import io
    decoded = base64.b64decode(content_string)
    
    # Save the file
    temp_file = os.path.join(OUTPUT_DIR, "temp_" + filename)
    with open(temp_file, 'wb') as f:
        f.write(decoded)
    
    # Load and clean the data
    df = data_processor.load_data(temp_file)
    
    if df is None:
        return (
            html.Div([
                html.I(className="fas fa-exclamation-triangle me-2"),
                "Error: The uploaded file doesn't have the required columns (Symbol, Date, Open, High, Low, Close, Volume)."
            ], className="text-danger"),
            html.Div([
                html.P("File format is invalid. Please make sure your Excel file has the following columns:"),
                html.Ul([
                    html.Li("Symbol - Stock symbol (e.g., NEPSE)"),
                    html.Li("Date - Trading date"),
                    html.Li("Open - Opening price"),
                    html.Li("High - Highest price"),
                    html.Li("Low - Lowest price"),
                    html.Li("Close - Closing price"),
                    html.Li("Volume - Trading volume")
                ])
            ]),
            {"display": "none"},
            True
        )
    
    cleaned_df = data_processor.clean_data(df)
    
    if cleaned_df is None or cleaned_df.empty:
        return (
            html.Div("Error processing file. Please check the data format.", className="text-danger"),
            html.Div("Unable to process the data. Make sure all numeric columns contain valid numbers."),
            {"display": "none"},
            True
        )
    
    # Store the data globally
    current_data = cleaned_df
    
    # Get dataset info
    dataset_info = data_processor.get_dataset_info(cleaned_df)
    
    # Create data preview
    preview = html.Div([
        html.H5(f"File: {filename}"),
        
        # Data summary
        html.Div([
            html.H6("Data Summary"),
            dbc.Row([
                dbc.Col([
                    html.P([
                        html.Strong("Date Range: "),
                        dataset_info["date_range"]
                    ])
                ], md=6),
                dbc.Col([
                    html.P([
                        html.Strong("Total Days: "),
                        f"{dataset_info['total_rows']}"
                    ])
                ], md=6)
            ]),
            dbc.Row([
                dbc.Col([
                    html.P([
                        html.Strong("Price Range: "),
                        f"{dataset_info['min_close']:.2f} - {dataset_info['max_close']:.2f}"
                    ])
                ], md=6),
                dbc.Col([
                    html.P([
                        html.Strong("Average Volume: "),
                        f"{dataset_info['avg_volume']:.2f}"
                    ])
                ], md=6)
            ]),
            
            # Show the first 5 rows of data
            html.Div([
                html.H6("Sample Data (First 5 Rows)"),
                dbc.Table.from_dataframe(
                    cleaned_df.head(5).round(2),
                    striped=True,
                    bordered=True,
                    hover=True,
                    responsive=True
                )
            ])
        ])
    ])
    
    return (
        html.Div([
            html.I(className="fas fa-check-circle me-2"),
            f"Successfully loaded {filename}"
        ], className="text-success"),
        preview,
        {"display": "block"},
        False
    )

# Callback for training and prediction
@app.callback(
    [Output("results-container", "style"),
     Output("prediction-chart", "figure"),
     Output("technical-chart", "figure"),
     Output("performance-chart", "figure"),
     Output("correlation-chart", "figure"),
     Output("trend-analysis-chart", "figure"),
     Output("training-accuracy", "children"),
     Output("testing-accuracy", "children"),
     Output("prediction-trend", "children"),
     Output("future-change", "children")],
    [Input("train-button", "n_clicks")],
    [State("time-step", "value"),
     State("prediction-days", "value"),
     State("train-ratio", "value"),
     State("model-type", "value")]
)
def train_and_predict(n_clicks, time_step, prediction_days, train_ratio, model_type):
    global current_data, trained_model, model_history, training_predictions, testing_predictions, future_predictions
    
    if n_clicks is None or current_data is None:
        raise PreventUpdate
    
    # Check if we have enough data
    if len(current_data) <= time_step:
        # Not enough data, return empty figures
        return (
            {"display": "none"},
            go.Figure(),
            go.Figure(),
            go.Figure(),
            go.Figure(),
            go.Figure(),
            "0%",
            "0%",
            "-",
            "0%"
        )
    
    # Prepare data for model
    X_train, X_test, y_train, y_test, prices = data_processor.prepare_for_lstm(current_data, time_step)
    
    # Create and train model based on user selection or compatibility
    try:
        if model_type == "lstm":
            # Try LSTM model first
            lstm_model = LSTMModel(time_step, prediction_days)
            history = lstm_model.train(X_train, y_train, X_test, y_test, epochs=50, batch_size=32)
            trained_model = lstm_model
        else:
            # Use SimpleRNN model
            simple_model = SimpleLSTMModel(time_step, prediction_days)
            history = simple_model.train(X_train, y_train, X_test, y_test, epochs=50, batch_size=32)
            trained_model = simple_model
    except Exception as e:
        # If LSTM fails, fall back to SimpleRNN
        print(f"Error with selected model: {e}. Falling back to SimpleRNN model.")
        simple_model = SimpleLSTMModel(time_step, prediction_days)
        history = simple_model.train(X_train, y_train, X_test, y_test, epochs=50, batch_size=32)
        trained_model = simple_model
    
    # Store history
    model_history = history
    
    # Make predictions
    train_predict = trained_model.predict(X_train)
    test_predict = trained_model.predict(X_test)
    
    # Inverse transform predictions
    train_predict = data_processor.inverse_transform(train_predict)
    test_predict = data_processor.inverse_transform(test_predict)
    
    # Store predictions
    training_predictions = train_predict
    testing_predictions = test_predict
    
    # Get future predictions
    last_sequence = current_data['Close'].values[-time_step:]
    future_preds = trained_model.predict_future(
        data_processor.scaler.transform(last_sequence.reshape(-1, 1)).flatten(),
        data_processor.scaler,
        prediction_days
    )
    
    # Store future predictions
    future_predictions = future_preds
    
    # Create future dates for prediction
    last_date = current_data['Date'].iloc[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=prediction_days)
    
    # Create visualizations
    prediction_fig = visualizer.create_prediction_plot(
        current_data['Date'],
        prices,
        train_predict,
        test_predict,
        future_dates,
        future_predictions
    )
    
    # Technical analysis chart
    technical_fig = visualizer.create_technical_analysis_plot(current_data)
    
    # Model performance chart
    performance_fig = visualizer.create_performance_metrics_chart(history)
    
    # Correlation heatmap
    correlation_fig = visualizer.create_correlation_heatmap(current_data)
    
    # Trend analysis chart
    trend_fig = go.Figure()
    
    # Add actual prices for the last 60 days
    last_days = min(60, len(current_data))
    trend_fig.add_trace(go.Scatter(
        x=current_data['Date'].iloc[-last_days:],
        y=current_data['Close'].iloc[-last_days:],
        mode='lines',
        name=f'Last {last_days} Days',
        line=dict(color=visualizer.colors['primary'], width=2)
    ))
    
    # Add future predictions
    trend_fig.add_trace(go.Scatter(
        x=future_dates,
        y=future_predictions.flatten(),
        mode='lines',
        name=f'Next {prediction_days} Days Prediction',
        line=dict(color=visualizer.colors['danger'], width=2, dash='dash')
    ))
    
    trend_fig.update_layout(
        title=f'Trend Analysis: Last {last_days} Days vs Next {prediction_days} Days Prediction',
        xaxis_title='Date',
        yaxis_title='Stock Price',
        template='plotly_white',
        hovermode='x unified'
    )
    
    # Calculate metrics
    # Calculate model accuracy (using RMSE/Mean as percentage)
    y_train_actual = data_processor.inverse_transform(y_train.reshape(-1, 1))
    y_test_actual = data_processor.inverse_transform(y_test.reshape(-1, 1))
    
    train_rmse = np.sqrt(np.mean(np.square(y_train_actual - train_predict)))
    test_rmse = np.sqrt(np.mean(np.square(y_test_actual - test_predict)))
    
    train_accuracy = max(0, 100 - (train_rmse / np.mean(y_train_actual) * 100))
    test_accuracy = max(0, 100 - (test_rmse / np.mean(y_test_actual) * 100))
    
    # Determine trend
    first_prediction = future_predictions[0][0]
    last_prediction = future_predictions[-1][0]
    
    if last_prediction > first_prediction:
        trend = "Bullish ▲"
    elif last_prediction < first_prediction:
        trend = "Bearish ▼"
    else:
        trend = "Neutral ◆"
    
    # Calculate percentage change
    change_pct = ((last_prediction - first_prediction) / first_prediction) * 100
    
    return (
        {"display": "block"},
        prediction_fig,
        technical_fig,
        performance_fig,
        correlation_fig,
        trend_fig,
        f"{train_accuracy:.2f}%",
        f"{test_accuracy:.2f}%",
        trend,
        f"{change_pct:.2f}%"
    )

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 