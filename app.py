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

# Sample data configurations
SAMPLE_DATA_PATH = "../testdata"
SAMPLE_DATA_FILES = {
    "CHCL": {
        "file": "CHCL_2022-02-08_2025-05-28.xlsx",
        "title": "Chilime Hydropower Limited (CHCL)",
        "description": "Leading hydropower company generating clean energy in Nepal",
        "sector": "Energy/Hydropower"
    },
    "HYDROPOWER": {
        "file": "HYDROPOWER_2022-02-08_2025-05-28.xlsx", 
        "title": "Hydropower Sector Index",
        "description": "Composite index of major hydropower companies in Nepal",
        "sector": "Energy/Hydropower"
    },
    "NABIL": {
        "file": "NABIL_2022-02-08_2025-05-28.xlsx",
        "title": "Nabil Bank Limited (NABIL)",
        "description": "Leading commercial bank with extensive branch network",
        "sector": "Banking"
    },
    "NEPSE": {
        "file": "NEPSE_2022-02-08_2025-05-28.xlsx",
        "title": "NEPSE Index",
        "description": "Main benchmark index of Nepal Stock Exchange",
        "sector": "Market Index"
    }
}

# Initialize Flask server for authentication integration
import flask
from auth import AuthManager, is_session_valid, clear_session

# Initialize Flask server
server = flask.Flask(__name__)
auth_manager = AuthManager(server)

# Initialize the Dash app with authentication support
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Stocks AI - NEPSE Market Prediction"

# Global variables to store data and model
current_data = None
trained_model = None
model_history = None
training_predictions = None
testing_predictions = None
future_predictions = None

# App layout with modern glassmorphic design
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # Hidden div to store sample data
    html.Div(id='sample-data-store', style={'display': 'none'}),
    
    # Header with user info
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1([
                        "Stocks ", html.Span("AI", style={"color": "#18BC9C"}),
                    ], className="header-title"),
                    html.P("NEPSE Market Prediction", className="header-subtitle")
                ], md=8),
                dbc.Col([
                    html.Div([
                        html.Div(id="user-info", style={"text-align": "right"}),
                        html.Button("Logout", id="logout-btn", className="btn btn-secondary", 
                                  style={"margin-top": "0.5rem"})
                    ])
                ], md=4, style={"display": "flex", "align-items": "center", "justify-content": "flex-end"})
            ])
        ])
    ], className="app-header mb-4"),
    
    # Main content
    dbc.Container([
        # Dashboard Grid
        html.Div([
            # File upload section
            html.Div([
                html.Div([
                    html.H4("Upload Stock Data", style={"color": "var(--text-primary)", "margin-bottom": "1.5rem"}),
                    html.Div([
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                html.Div("📈", className="upload-box-icon"),
                                html.Div('Drag and drop a file here', className="upload-text"),
                                html.Div('e.xlsx...csv', className="upload-hint")
                            ]),
                            className="upload-box"
                        )
                    ]),
                    
                    # Test Sample Data Button
                    html.Div([
                        html.Hr(style={"margin": "2rem 0", "border-color": "rgba(255, 255, 255, 0.1)"}),
                        html.Div([
                            html.Span("OR", style={
                                "background": "var(--card-bg)", 
                                "padding": "0 1rem", 
                                "color": "var(--text-secondary)",
                                "font-weight": "500"
                            })
                        ], style={"text-align": "center", "margin": "-1rem 0 2rem 0"}),
                        
                        html.Button([
                            html.Span("🧪", className="icon"),
                            "Test Sample DATA"
                        ], id="test-sample-btn", className="test-sample-btn")
                    ]),
                    
                    html.Div(id='upload-output', className="mt-3"),
                    
                    # Expected format helper
                    html.Div([
                        html.H6("Accepted file formats:", style={"color": "var(--text-secondary)", "margin-top": "1rem"}),
                        html.P("Your Excel file should include these columns:", 
                               style={"color": "var(--text-muted)", "font-size": "0.9rem"}),
                        html.Div([
                            html.Table([
                                html.Thead(
                                    html.Tr([
                                        html.Th("Symbol", style={"color": "var(--text-secondary)"}), 
                                        html.Th("Date", style={"color": "var(--text-secondary)"}), 
                                        html.Th("Open", style={"color": "var(--text-secondary)"}), 
                                        html.Th("High", style={"color": "var(--text-secondary)"}), 
                                        html.Th("Low", style={"color": "var(--text-secondary)"}), 
                                        html.Th("Close", style={"color": "var(--text-secondary)"}), 
                                        html.Th("Volume", style={"color": "var(--text-secondary)"})
                                    ])
                                ),
                                html.Tbody([
                                    html.Tr([
                                        html.Td("NEPSE", style={"color": "var(--text-primary)"}), 
                                        html.Td("2025-04-12", style={"color": "var(--text-primary)"}), 
                                        html.Td("2677.58", style={"color": "var(--text-primary)"}), 
                                        html.Td("2687.92", style={"color": "var(--text-primary)"}), 
                                        html.Td("2667.00", style={"color": "var(--text-primary)"}), 
                                        html.Td("2670.77", style={"color": "var(--text-primary)"}), 
                                        html.Td("5,637,981,250.23", style={"color": "var(--text-primary)"})
                                    ])
                                ])
                            ], className="data-table")
                        ])
                    ], id="format-helper", className="mt-3"),
                ], className="glass-card")
            ], className="mb-4"),
            
            # Sample Data Selection Modal
            dbc.Modal([
                dbc.ModalHeader([
                    html.H4("Select Sample Data", style={"color": "var(--text-primary)"})
                ]),
                dbc.ModalBody([
                    html.Div([
                        html.P("Choose from our curated sample datasets to test the AI model:", 
                               style={"color": "var(--text-secondary)", "margin-bottom": "2rem"}),
                        html.Div(id="sample-data-cards", className="sample-data-grid")
                    ])
                ]),
                dbc.ModalFooter([
                    html.Button("Close", id="close-sample-modal", className="btn btn-secondary")
                ])
            ], id="sample-data-modal", size="xl", is_open=False, style={"--bs-modal-bg": "var(--card-bg)"}),
            
            # Model parameters section
            html.Div([
                html.Div([
                    html.H4("Model Parameters", style={"color": "var(--text-primary)", "margin-bottom": "1.5rem"}),
                    html.Div([
                        html.Div([
                            html.Label("Time Step", className="form-label"),
                            dbc.Input(id="time-step", type="number", value=60, min=1, max=200, className="form-control")
                        ], className="form-group"),
                        html.Div([
                            html.Label("Prediction Days", className="form-label"),
                            dbc.Input(id="prediction-days", type="number", value=30, min=1, max=90, className="form-control")
                        ], className="form-group"),
                        html.Div([
                            html.Label("Training Ratio", className="form-label"),
                            dbc.Input(id="train-ratio", type="number", value=0.8, min=0.5, max=0.9, step=0.05, className="form-control")
                        ], className="form-group"),
                        html.Div([
                            html.Label("Model Type", className="form-label"),
                            dbc.Select(
                                id="model-type",
                                options=[
                                    {"label": "LSTM Complex", "value": "lstm"},
                                    {"label": "SimpleRNN Compatible", "value": "simple"}
                                ],
                                value="simple",
                                className="form-control"
                            )
                        ], className="form-group"),
                        
                        # Train button
                        html.Div([
                            html.Button("Train Model & Predict", 
                                      id="train-button", 
                                      className="btn btn-primary",
                                      disabled=True)
                        ], className="mt-3")
                    ])
                ], className="glass-card")
            ], id="model-params-container", style={"display": "none"}, className="mb-4"),
            
        ], className="dashboard-grid"),
        
        # Data preview section
        html.Div([
            html.Div([
                html.H4("Data Preview", style={"color": "var(--text-primary)", "margin-bottom": "1.5rem"}),
                dcc.Loading(
                    id="loading-data-preview",
                    type="default",
                    children=[
                        html.Div(id="data-preview-container", 
                                style={"color": "var(--text-secondary)"})
                    ]
                )
            ], className="glass-card")
        ], className="mb-4"),
        
        # Model training and prediction section (appears after training)
        html.Div([
            # Stats cards
            html.Div([
                html.Div([
                    html.Div(html.H4(id="training-accuracy", children="0%"), 
                             className="stats-card-value"),
                    html.Div("Training Accuracy", className="stats-card-title")
                ], className="stats-card success"),
                html.Div([
                    html.Div(html.H4(id="testing-accuracy", children="0%"), 
                             className="stats-card-value"),
                    html.Div("Testing Accuracy", className="stats-card-title")
                ], className="stats-card warning"),
                html.Div([
                    html.Div(html.H4(id="prediction-trend", children="-"), 
                             className="stats-card-value"),
                    html.Div("Predicted Trend", className="stats-card-title")
                ], className="stats-card secondary"),
                html.Div([
                    html.Div(html.H4(id="future-change", children="0%"), 
                             className="stats-card-value"),
                    html.Div("Predicted Change", className="stats-card-title")
                ], className="stats-card primary")
            ], className="stats-grid"),
            
            # Trend analysis chart
            html.Div([
                html.Div([
                    html.H4("Trend Analysis", style={"color": "var(--text-primary)"}),
                    dcc.Graph(id="trend-analysis-chart")
                ], className="glass-card")
            ], className="mb-4"),
            
            # Visualization tabs
            html.Div([
                html.Div([
                    # Tabs for different visualizations
                    html.Div([
                        html.Button("Price Prediction", id="tab-prediction", className="tab active"),
                        html.Button("Technical Analysis", id="tab-technical", className="tab"),
                        html.Button("Model Performance", id="tab-performance", className="tab"),
                        html.Button("Correlation Analysis", id="tab-correlation", className="tab")
                    ], className="tabs-container"),
                    
                    # Tab content
                    html.Div([
                        dcc.Graph(id="prediction-chart", style={"display": "block"}),
                        dcc.Graph(id="technical-chart", style={"display": "none"}),
                        dcc.Graph(id="performance-chart", style={"display": "none"}),
                        dcc.Graph(id="correlation-chart", style={"display": "none"})
                    ])
                ], className="glass-card")
            ])
        ], id="results-container", style={"display": "none"}),
        
        # Footer
        html.Footer([
            html.P([
                "Stocks AI - NEPSE Market Prediction © ", 
                str(datetime.datetime.now().year)
            ], style={"color": "var(--text-secondary)", "text-align": "center", "margin": "2rem 0"}),
        ])
    ], fluid=True)
])

# User session and authentication callbacks
@app.callback(
    Output("user-info", "children"),
    [Input("url", "href")]  # We'll add this input to the layout
)
def update_user_info(href):
    """Update user info display"""
    try:
        if is_session_valid():
            from flask import session
            user_name = session.get('user_name', 'User')
            user_email = session.get('user_email', '')
            return html.Div([
                html.P(f"Welcome, {user_name}!", 
                       style={"color": "var(--text-primary)", "margin": "0", "font-weight": "500"}),
                html.P(user_email, 
                       style={"color": "var(--text-secondary)", "margin": "0", "font-size": "0.8rem"})
            ])
        else:
            return html.Div([
                html.P("Please login to continue", 
                       style={"color": "var(--text-secondary)", "margin": "0"}),
                html.A("Login", href="http://127.0.0.1:8060", target="_blank",
                       className="btn btn-primary", style={"margin-top": "0.5rem", "font-size": "0.8rem"})
            ])
    except Exception:
        return html.Div([
            html.P("Please login to continue", 
                   style={"color": "var(--text-secondary)", "margin": "0"}),
            html.A("Login", href="http://127.0.0.1:8060", target="_blank",
                   className="btn btn-primary", style={"margin-top": "0.5rem", "font-size": "0.8rem"})
        ])

@app.callback(
    Output("url", "href"),
    [Input("logout-btn", "n_clicks")],
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    """Handle user logout"""
    if n_clicks:
        clear_session()
        return "http://127.0.0.1:8060"  # Redirect to auth page
    raise PreventUpdate

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
    
    # Trend analysis chart with dark theme
    trend_fig = visualizer.create_trend_analysis_chart(current_data.copy())
    
    # Calculate accuracy metrics
    if len(test_predict) > 0 and len(y_test) > 0:
        # Calculate RMSE-based accuracy
        train_rmse = np.sqrt(np.mean((train_predict.flatten() - data_processor.inverse_transform(y_train.reshape(-1, 1)).flatten()) ** 2))
        test_rmse = np.sqrt(np.mean((test_predict.flatten() - data_processor.inverse_transform(y_test.reshape(-1, 1)).flatten()) ** 2))
        
        # Convert RMSE to percentage accuracy (simplified metric)
        avg_price = np.mean(prices)
        train_accuracy = max(0, (1 - train_rmse / avg_price) * 100)
        test_accuracy = max(0, (1 - test_rmse / avg_price) * 100)
    else:
        train_accuracy = 0
        test_accuracy = 0
    
    # Calculate prediction trend
    if len(future_predictions) > 1:
        current_price = current_data['Close'].iloc[-1]
        future_price = future_predictions[-1][0]
        change_percent = ((future_price - current_price) / current_price) * 100
        
        if change_percent > 2:
            trend = "📈 Bullish"
        elif change_percent < -2:
            trend = "📉 Bearish"
        else:
            trend = "➡️ Neutral"
        
        future_change = f"{change_percent:+.1f}%"
    else:
        trend = "-"
        future_change = "0%"
    
    return (
        {"display": "block"},
        prediction_fig,
        technical_fig,
        performance_fig,
        correlation_fig,
        trend_fig,
        f"{train_accuracy:.1f}%",
        f"{test_accuracy:.1f}%",
        trend,
        future_change
    )

# Tab switching callback
@app.callback(
    [Output("prediction-chart", "style"),
     Output("technical-chart", "style"),
     Output("performance-chart", "style"),
     Output("correlation-chart", "style"),
     Output("tab-prediction", "className"),
     Output("tab-technical", "className"),
     Output("tab-performance", "className"),
     Output("tab-correlation", "className")],
    [Input("tab-prediction", "n_clicks"),
     Input("tab-technical", "n_clicks"),
     Input("tab-performance", "n_clicks"),
     Input("tab-correlation", "n_clicks")]
)
def switch_tabs(pred_clicks, tech_clicks, perf_clicks, corr_clicks):
    ctx = callback_context
    if not ctx.triggered:
        return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}, "tab active", "tab", "tab", "tab"
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # Reset all displays and classes
    displays = [{"display": "none"}] * 4
    classes = ["tab"] * 4
    
    # Set active tab
    if triggered_id == "tab-prediction":
        displays[0] = {"display": "block"}
        classes[0] = "tab active"
    elif triggered_id == "tab-technical":
        displays[1] = {"display": "block"}
        classes[1] = "tab active"
    elif triggered_id == "tab-performance":
        displays[2] = {"display": "block"}
        classes[2] = "tab active"
    elif triggered_id == "tab-correlation":
        displays[3] = {"display": "block"}
        classes[3] = "tab active"
    
    return displays + classes

# Sample data callbacks
@app.callback(
    [Output("sample-data-modal", "is_open"),
     Output("sample-data-cards", "children")],
    [Input("test-sample-btn", "n_clicks"),
     Input("close-sample-modal", "n_clicks")],
    [State("sample-data-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_sample_modal(test_clicks, close_clicks, is_open):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id == "test-sample-btn":
        # Create sample data cards
        cards = []
        for key, config in SAMPLE_DATA_FILES.items():
            card = html.Div([
                html.Div([
                    html.H5(config["title"], className="sample-data-title"),
                    html.P(config["description"], className="sample-data-info"),
                    html.Div([
                        html.Span(f"Sector: {config['sector']}", style={"font-weight": "500"}),
                        html.Span("📊 Ready", style={"color": "var(--neon-green)"})
                    ], className="sample-data-stats")
                ])
            ], className="sample-data-card", id={"type": "sample-card", "index": key})
            cards.append(card)
        
        return True, cards
    
    elif triggered_id == "close-sample-modal":
        return False, []
    
    return is_open, []

@app.callback(
    [Output("upload-output", "children", allow_duplicate=True),
     Output("data-preview-container", "children", allow_duplicate=True),
     Output("model-params-container", "style", allow_duplicate=True),
     Output("train-button", "disabled", allow_duplicate=True),
     Output("sample-data-modal", "is_open", allow_duplicate=True)],
    [Input({"type": "sample-card", "index": dash.dependencies.ALL}, "n_clicks")],
    prevent_initial_call=True
)
def handle_sample_data_selection(n_clicks_list):
    global current_data
    
    ctx = callback_context
    if not ctx.triggered or not any(n_clicks_list):
        raise PreventUpdate
    
    # Get the clicked card index
    triggered_prop_id = ctx.triggered[0]['prop_id']
    import json
    clicked_index = json.loads(triggered_prop_id.split('.')[0])['index']
    
    try:
        # Load the selected sample data
        config = SAMPLE_DATA_FILES[clicked_index]
        file_path = os.path.join(SAMPLE_DATA_PATH, config["file"])
        
        if not os.path.exists(file_path):
            return (
                html.Div([
                    html.P("❌ Sample data file not found", style={"color": "#E74C3C"}),
                    html.P(f"Looking for: {file_path}", style={"color": "var(--text-muted)", "font-size": "0.8rem"})
                ]),
                None, {"display": "none"}, True, False
            )
        
        # Load and process the data
        df = data_processor.load_data(file_path)
        if df is None:
            return (
                html.Div([
                    html.P("❌ Failed to load sample data", style={"color": "#E74C3C"})
                ]),
                None, {"display": "none"}, True, False
            )
        
        # Clean the data
        df_cleaned = data_processor.clean_data(df)
        if df_cleaned is None:
            return (
                html.Div([
                    html.P("❌ Failed to process sample data", style={"color": "#E74C3C"})
                ]),
                None, {"display": "none"}, True, False
            )
        
        current_data = df_cleaned
        dataset_info = data_processor.get_dataset_info(df_cleaned)
        
        # Create upload success message
        upload_output = html.Div([
            html.Div([
                html.H5([
                    html.Span("✅ ", style={"color": "#2ECC71"}),
                    f"Sample Data Loaded: {config['title']}"
                ], style={"color": "var(--text-primary)", "margin-bottom": "1rem"}),
                html.P(config["description"], style={"color": "var(--text-secondary)", "margin-bottom": "0.5rem"}),
                html.P(f"Sector: {config['sector']}", style={"color": "var(--text-muted)", "font-size": "0.9rem"})
            ], className="alert alert-success", style={
                "background": "rgba(46, 204, 113, 0.1)",
                "border": "1px solid rgba(46, 204, 113, 0.3)",
                "border-radius": "12px",
                "padding": "1rem"
            })
        ])
        
        # Create data preview
        preview_table = html.Div([
            html.H5(f"Dataset Overview - {dataset_info['total_rows']} records", 
                   style={"color": "var(--text-primary)", "margin-bottom": "1rem"}),
            
            # Stats row
            html.Div([
                html.Div([
                    html.H6("Date Range", style={"color": "var(--text-secondary)", "margin-bottom": "0.5rem"}),
                    html.P(dataset_info['date_range'], style={"color": "var(--text-primary)", "font-weight": "500"})
                ], className="col-md-3"),
                html.Div([
                    html.H6("Price Range", style={"color": "var(--text-secondary)", "margin-bottom": "0.5rem"}),
                    html.P(f"${dataset_info['min_close']:.2f} - ${dataset_info['max_close']:.2f}", 
                          style={"color": "var(--text-primary)", "font-weight": "500"})
                ], className="col-md-3"),
                html.Div([
                    html.H6("Average Price", style={"color": "var(--text-secondary)", "margin-bottom": "0.5rem"}),
                    html.P(f"${dataset_info['avg_close']:.2f}", 
                          style={"color": "var(--text-primary)", "font-weight": "500"})
                ], className="col-md-3"),
                html.Div([
                    html.H6("Avg Volume", style={"color": "var(--text-secondary)", "margin-bottom": "0.5rem"}),
                    html.P(f"{dataset_info['avg_volume']:,.0f}", 
                          style={"color": "var(--text-primary)", "font-weight": "500"})
                ], className="col-md-3")
            ], className="row mb-3"),
            
            # Sample data table
            html.Div([
                html.H6("Sample Data (First 10 rows)", style={"color": "var(--text-secondary)", "margin-bottom": "1rem"}),
                html.Table([
                    html.Thead(
                        html.Tr([
                            html.Th(col, style={"color": "var(--text-secondary)", "padding": "0.75rem"}) 
                            for col in df_cleaned.columns[:6]  # Show first 6 columns
                        ])
                    ),
                    html.Tbody([
                        html.Tr([
                            html.Td(str(df_cleaned.iloc[i][col])[:20] + ("..." if len(str(df_cleaned.iloc[i][col])) > 20 else ""), 
                                   style={"color": "var(--text-primary)", "padding": "0.75rem"}) 
                            for col in df_cleaned.columns[:6]
                        ]) for i in range(min(10, len(df_cleaned)))
                    ])
                ], className="data-table", style={"width": "100%"})
            ])
        ])
        
        return (
            upload_output,
            preview_table,
            {"display": "block"},
            False,
            False
        )
        
    except Exception as e:
        return (
            html.Div([
                html.P("❌ Error loading sample data", style={"color": "#E74C3C"}),
                html.P(f"Error details: {str(e)}", style={"color": "var(--text-muted)", "font-size": "0.8rem"})
            ]),
            None, {"display": "none"}, True, False
        )

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 