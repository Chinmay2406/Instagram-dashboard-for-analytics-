import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests  # For data fetching (if scraping or API usage is allowed)
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

# Function to fetch Instagram data (replace with actual scraping or API logic)
def fetch_instagram_data(profile_url):
    # Here you would implement your logic to scrape or get data from the Instagram profile
    # For demonstration, we will return mock data
    mock_data = {
        "username": "example_user",
        "followers": 1500,
        "likes": [20, 30, 50, 70, 90],  # Mock likes over the last 5 posts
        "comments": [5, 10, 15, 20, 25],  # Mock comments over the last 5 posts
        "follower_growth": [1400, 1450, 1470, 1480, 1500],  # Mock growth data
        "bio": "This is a mock bio for the example user.",
        "profile_picture": "https://via.placeholder.com/150"
    }
    return mock_data

# Define the layout of the app
app.layout = html.Div([
    html.H1("Instagram Analytics Dashboard", style={'textAlign': 'center'}),
    dcc.Input(
        id='input-url', 
        type='text', 
        placeholder='Paste your Instagram profile URL...', 
        style={'width': '50%', 'margin-bottom': '20px'}
    ),
    html.Button('Fetch Data', id='fetch-btn', n_clicks=0),
    html.Div(id='account-info', style={'margin-top': '20px'}),
    dcc.Graph(id='followers-growth'),
    dcc.Graph(id='likes-comments'),
])

# Define callback to update account info and graphs based on user input
@app.callback(
    Output('account-info', 'children'),
    Output('followers-growth', 'figure'),
    Output('likes-comments', 'figure'),
    Input('fetch-btn', 'n_clicks'),
    State('input-url', 'value')
)
def update_output(n_clicks, profile_url):
    if n_clicks > 0 and profile_url:
        # Fetch the data
        data = fetch_instagram_data(profile_url)

        # Create figures for graphs
        followers_growth_fig = go.Figure()
        followers_growth_fig.add_trace(go.Scatter(
            x=list(range(1, len(data['follower_growth']) + 1)),
            y=data['follower_growth'],
            mode='lines+markers',
            name='Follower Growth'
        ))
        followers_growth_fig.update_layout(title='Follower Growth Over Time', xaxis_title='Time', yaxis_title='Followers')

        likes_comments_fig = go.Figure()
        likes_comments_fig.add_trace(go.Bar(
            x=list(range(1, len(data['likes']) + 1)),
            y=data['likes'],
            name='Likes'
        ))
        likes_comments_fig.add_trace(go.Bar(
            x=list(range(1, len(data['comments']) + 1)),
            y=data['comments'],
            name='Comments'
        ))
        likes_comments_fig.update_layout(title='Likes and Comments on Last Posts', barmode='group', xaxis_title='Posts', yaxis_title='Count')

        # Display account information
        account_info = html.Div([
            html.Img(src=data['profile_picture'], style={'width': '100px', 'height': '100px'}),
            html.H2(data['username']),
            html.P(data['bio']),
            html.P(f"Followers: {data['followers']}")
        ])

        return account_info, followers_growth_fig, likes_comments_fig
    return html.Div(), go.Figure(), go.Figure()

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
