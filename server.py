from flask import Flask
from dash import Dash

# Initialize Flask server
server = Flask(__name__)

# Initialize Dash app
app = Dash(__name__, server=server, suppress_callback_exceptions=True)

if __name__ == '__main__':
    server.run(debug=True)
