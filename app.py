import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
from datetime import date
from server import server  # Import the server

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], server=server)

# Home Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col(html.Img(src='/assets/instagram_logo.png', height='100px'), width='auto'),
        dbc.Col(html.H1("Welcome to the Instagram Dashboard!", className='text-center'), width=True),
    ], align='center'),
    html.Div(className='navigation-panel', style={'textAlign': 'left'}),
    dcc.Link('Analytics', href='/analytics', className='nav-link'),
    dcc.Link('Tips', href='/tips', className='nav-link'),
    dcc.Link('Content Calendar', href='/calendar', className='nav-link'),
    dcc.Link('Chatbot', href='/chatbot', className='nav-link'),
    html.Div(id='page-content')
])

# Callback to render the appropriate page
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/analytics':
        return analytics_layout()
    elif pathname == '/tips':
        return tips_layout()
    elif pathname == '/calendar':
        return calendar_layout()
    elif pathname == '/chatbot':
        return chatbot_layout()
    else:
        return html.Div([html.H2("Welcome! Please select a section.")])

# Analytics Layout
def analytics_layout():
    return html.Div([
        html.H2("Instagram Analytics"),
        dcc.Input(id='profile-url', type='text', placeholder='Enter Instagram Profile URL', style={'margin': '10px'}),
        html.Button('Submit', id='submit-url', n_clicks=0),
        html.Div(id='analytics-output'),
    ])

@app.callback(
    Output('analytics-output', 'children'),
    Input('submit-url', 'n_clicks'),
    State('profile-url', 'value')
)
def update_analytics(n_clicks, url):
    if n_clicks <= 0:
        return ""
    
    # Placeholder for data retrieval logic
    data = {
        'Followers': [150, 200, 250, 300, 350],
        'Views': [100, 150, 200, 250, 300],
        'Positive Comments': [10, 20, 30, 40, 50],
        'Negative Comments': [1, 2, 1, 3, 2],
    }
    
    df = pd.DataFrame(data)
    
    # Create a line chart for followers over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Followers'], mode='lines+markers', name='Followers'))
    fig.add_trace(go.Scatter(x=df.index, y=df['Views'], mode='lines+markers', name='Views'))
    fig.update_layout(title='Instagram Analytics', xaxis_title='Time', yaxis_title='Count')
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.P(f"Profile URL: {url}")
    ])

# Tips Layout
def tips_layout():
    return html.Div([
        html.H2("Growth Tips"),
        html.Div(id='tips-output'),
        html.Button('Get Tips', id='get-tips', n_clicks=0),
    ])

@app.callback(
    Output('tips-output', 'children'),
    Input('get-tips', 'n_clicks')
)
def display_tips(n_clicks):
    if n_clicks <= 0:
        return ""
    
    tips = [
        "Engage with your audience by responding to comments.",
        "Use high-quality images and videos.",
        "Post consistently and use Instagram stories.",
        "Collaborate with influencers in your niche.",
        "Utilize Instagram analytics to improve your strategy."
    ]
    
    return html.Div([html.P(tip) for tip in tips])

# Content Calendar Layout
def calendar_layout():
    return html.Div([
        html.H2("Content Calendar"),
        dcc.DatePickerRange(
            id='date-picker-range',
            start_date=date.today(),
            end_date=date(2025, 12, 31)
        ),
        dcc.Input(id='reminder-input', type='text', placeholder='Enter Reminder', style={'margin': '10px'}),
        html.Button('Save Reminder', id='save-reminder', n_clicks=0),
        html.Div(id='calendar-output'),
    ])

@app.callback(
    Output('calendar-output', 'children'),
    Input('save-reminder', 'n_clicks'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date'),
    State('reminder-input', 'value')
)
def save_reminder(n_clicks, start_date, end_date, reminder):
    if n_clicks <= 0:
        return ""
    
    return f"Reminder '{reminder}' saved for {start_date} to {end_date}."

# Chatbot Layout
def chatbot_layout():
    return html.Div([
        html.H2("Chatbot"),
        dcc.Input(id='chat-input', type='text', placeholder='Ask a question...', style={'margin': '10px'}),
        html.Button('Send', id='send-button', n_clicks=0),
        html.Div(id='chat-output'),
    ])

@app.callback(
    Output('chat-output', 'children'),
    Input('send-button', 'n_clicks'),
    State('chat-input', 'value')
)
def respond_to_chat(n_clicks, question):
    if n_clicks <= 0 or not question:
        return ""
    
    # Placeholder for chatbot logic
    response = f"You asked: {question}. Here is a general response."
    
    return html.Div([html.P(response)])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
