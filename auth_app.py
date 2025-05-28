"""
Authentication Application for StockAI
Provides login/signup pages with modern glassmorphic design
"""

import dash
from dash import dcc, html, Input, Output, State, callback_context, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import flask
from flask_login import current_user, login_required
import webbrowser
from threading import Timer

from auth import AuthManager, create_secure_session, clear_session

# Initialize Flask app
server = flask.Flask(__name__)
auth_manager = AuthManager(server)

# Initialize Dash app
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True,
    assets_folder='assets'
)

app.title = "StockAI - Login"

# Auth page layout matching the reference UI
auth_layout = html.Div([
    html.Div([
        html.Div([
            # Logo and title
            html.H1([
                "Stocks ", html.Span("AI", style={"color": "#18BC9C"}),
            ], className="header-title"),
            html.P("NEPSE Market Prediction", className="header-subtitle"),
            
            # Auth tabs
            html.Div([
                html.Button("Login", id="login-tab", className="auth-tab active"),
                html.Button("Sign Up", id="signup-tab", className="auth-tab")
            ], className="auth-tabs"),
            
            # Login form
            html.Div([
                html.Div([
                    html.Label("Email", className="form-label"),
                    dcc.Input(
                        id="login-email",
                        type="email",
                        placeholder="Enter your email",
                        className="form-control"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Password", className="form-label"),
                    dcc.Input(
                        id="login-password",
                        type="password",
                        placeholder="Enter your password",
                        className="form-control"
                    )
                ], className="form-group"),
                
                html.Button("Login", id="login-btn", className="btn btn-primary"),
                
                html.P([
                    "Don't have an account? ",
                    html.A("Sign Up", id="switch-to-signup", style={"color": "#18BC9C", "cursor": "pointer"})
                ], style={"margin-top": "1rem", "color": "var(--text-secondary)"})
            ], id="login-form", style={"display": "block"}),
            
            # Signup form
            html.Div([
                html.Div([
                    html.Label("First Name", className="form-label"),
                    dcc.Input(
                        id="signup-firstname",
                        type="text",
                        placeholder="Enter your first name",
                        className="form-control"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Last Name", className="form-label"),
                    dcc.Input(
                        id="signup-lastname",
                        type="text",
                        placeholder="Enter your last name",
                        className="form-control"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Email", className="form-label"),
                    dcc.Input(
                        id="signup-email",
                        type="email",
                        placeholder="Enter your email",
                        className="form-control"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Password", className="form-label"),
                    dcc.Input(
                        id="signup-password",
                        type="password",
                        placeholder="Create a password",
                        className="form-control"
                    )
                ], className="form-group"),
                
                html.Div([
                    html.Label("Confirm Password", className="form-label"),
                    dcc.Input(
                        id="signup-confirm-password",
                        type="password",
                        placeholder="Confirm your password",
                        className="form-control"
                    )
                ], className="form-group"),
                
                html.Button("Sign Up", id="signup-btn", className="btn btn-primary"),
                
                html.P([
                    "Already have an account? ",
                    html.A("Login", id="switch-to-login", style={"color": "#18BC9C", "cursor": "pointer"})
                ], style={"margin-top": "1rem", "color": "var(--text-secondary)"})
            ], id="signup-form", style={"display": "none"}),
            
            # Messages
            html.Div(id="auth-messages", className="mt-3")
            
        ], className="glass-card auth-card")
    ], className="auth-container")
])

# Main app layout with conditional rendering
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback to handle page routing
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    return auth_layout

# Tab switching callbacks
@app.callback(
    [Output('login-form', 'style'),
     Output('signup-form', 'style'),
     Output('login-tab', 'className'),
     Output('signup-tab', 'className')],
    [Input('login-tab', 'n_clicks'),
     Input('signup-tab', 'n_clicks'),
     Input('switch-to-signup', 'n_clicks'),
     Input('switch-to-login', 'n_clicks')]
)
def switch_auth_forms(login_clicks, signup_clicks, switch_signup, switch_login):
    ctx = callback_context
    if not ctx.triggered:
        return {"display": "block"}, {"display": "none"}, "auth-tab active", "auth-tab"
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_id in ['signup-tab', 'switch-to-signup']:
        return {"display": "none"}, {"display": "block"}, "auth-tab", "auth-tab active"
    else:
        return {"display": "block"}, {"display": "none"}, "auth-tab active", "auth-tab"

# Login callback
@app.callback(
    Output('auth-messages', 'children', allow_duplicate=True),
    [Input('login-btn', 'n_clicks')],
    [State('login-email', 'value'),
     State('login-password', 'value')],
    prevent_initial_call=True
)
def handle_login(n_clicks, email, password):
    if not n_clicks:
        raise PreventUpdate
    
    if not email or not password:
        return html.Div("Please fill in all fields", 
                       style={"color": "#E74C3C", "text-align": "center", "margin-top": "1rem"})
    
    success, message, user = auth_manager.login_user_func(email, password)
    
    if success:
        # Create secure session
        create_secure_session(user.id, {'user_email': user.email, 'user_name': user.get_full_name()})
        
        # Success message and redirect instruction
        return html.Div([
            html.Div("Login successful! 🎉", 
                    style={"color": "#2ECC71", "text-align": "center", "margin-bottom": "1rem"}),
            html.Div("Redirecting to dashboard...", 
                    style={"color": "var(--text-secondary)", "text-align": "center", "font-size": "0.9rem"}),
            dcc.Interval(id="redirect-interval", interval=2000, n_intervals=0, max_intervals=1)
        ])
    else:
        return html.Div(message, 
                       style={"color": "#E74C3C", "text-align": "center", "margin-top": "1rem"})

# Signup callback
@app.callback(
    Output('auth-messages', 'children', allow_duplicate=True),
    [Input('signup-btn', 'n_clicks')],
    [State('signup-firstname', 'value'),
     State('signup-lastname', 'value'),
     State('signup-email', 'value'),
     State('signup-password', 'value'),
     State('signup-confirm-password', 'value')],
    prevent_initial_call=True
)
def handle_signup(n_clicks, first_name, last_name, email, password, confirm_password):
    if not n_clicks:
        raise PreventUpdate
    
    # Validate input
    if not all([first_name, last_name, email, password, confirm_password]):
        return html.Div("Please fill in all fields", 
                       style={"color": "#E74C3C", "text-align": "center", "margin-top": "1rem"})
    
    if password != confirm_password:
        return html.Div("Passwords do not match", 
                       style={"color": "#E74C3C", "text-align": "center", "margin-top": "1rem"})
    
    success, message = auth_manager.register_user(email, password, first_name, last_name)
    
    if success:
        return html.Div([
            html.Div("Account created successfully! 🎉", 
                    style={"color": "#2ECC71", "text-align": "center", "margin-bottom": "0.5rem"}),
            html.Div("Please login with your credentials", 
                    style={"color": "var(--text-secondary)", "text-align": "center", "font-size": "0.9rem"})
        ])
    else:
        return html.Div(message, 
                       style={"color": "#E74C3C", "text-align": "center", "margin-top": "1rem"})

# Redirect callback (if login successful, show message to go to main app)
@app.callback(
    Output('auth-messages', 'children', allow_duplicate=True),
    [Input('redirect-interval', 'n_intervals')],
    prevent_initial_call=True
)
def redirect_to_dashboard(n_intervals):
    if n_intervals > 0:
        return html.Div([
            html.Div("✅ Login Successful!", 
                    style={"color": "#2ECC71", "text-align": "center", "margin-bottom": "1rem", "font-size": "1.2rem"}),
            html.Div("Now you can access the main application:", 
                    style={"color": "var(--text-secondary)", "text-align": "center", "margin-bottom": "1rem"}),
            html.A("🚀 Launch StockAI Dashboard", 
                  href="http://127.0.0.1:8050", 
                  target="_blank",
                  className="btn btn-primary",
                  style={"display": "block", "width": "100%", "text-decoration": "none"})
        ])
    raise PreventUpdate

# Flask routes for API endpoints
@server.route('/api/user-stats')
def get_user_stats():
    stats = auth_manager.get_user_stats()
    return flask.jsonify(stats)

@server.route('/api/logout', methods=['POST'])
def logout():
    auth_manager.logout_user_func()
    clear_session()
    return flask.jsonify({"success": True, "message": "Logged out successfully"})

@server.route('/health')
def health_check():
    return flask.jsonify({
        "status": "healthy",
        "database": "connected",
        "auth_system": "active"
    })

# Auto-open browser function
def open_browser():
    webbrowser.open_new("http://127.0.0.1:8060/")

if __name__ == '__main__':
    print("🔐 StockAI Authentication System")
    print("=" * 50)
    print("🎯 Starting secure authentication server...")
    print("🔗 Access URL: http://127.0.0.1:8060")
    print("🛡️  Database: SQLite with encrypted passwords")
    print("⚡ Features: Login, Signup, Session Management")
    print("=" * 50)
    
    # Print database security info
    from auth import DATABASE_SECURITY_INFO
    print(DATABASE_SECURITY_INFO)
    
    # Auto-open browser after a short delay
    Timer(1.5, open_browser).start()
    
    # Run the app
    app.run_server(debug=True, host='127.0.0.1', port=8060) 