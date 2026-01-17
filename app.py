import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from rtk_data import RTKMonitor
import time
import random

rtk = RTKMonitor()
app = dash.Dash(__name__)
app.title = "RTK Survey Dashboard - Ahmedabad"

app.layout = html.Div([
    html.H1("📱 Smartphone RTK Survey Dashboard", style={'textAlign': 'center'}),
    
    # Status Cards
    html.Div([
        html.Div([html.H2(id='status', children="Starting..."), html.P("RTK Status")], 
                 className='card', style={'background': '#27ae60'}),
        html.Div([html.H2(id='fix', children="Single"), html.P("Fix Type")], 
                 className='card', style={'background': '#f39c12'}),
        html.Div([html.H2(id='sats', children="0"), html.P("Satellites")], 
                 className='card', style={'background': '#3498db'})
    ], className='status-row'),
    
    dcc.Graph(id='live-map'),
    dcc.Graph(id='live-altitude'),
    
    dcc.Interval(id='live-update', interval=2000, n_intervals=0)
], className='container')

@app.callback(
    [Output('status', 'children'), Output('fix', 'children'), Output('sats', 'children'),
     Output('live-map', 'figure'), Output('live-altitude', 'figure')],
    [Input('live-update', 'n_intervals')]
)
def update_dashboard(n):
    rtk.update_data()
    
    # Status colors
    status_color = '#27ae60' if 'Fixed' in rtk.status else '#f39c12'
    
    # Map
    df = pd.DataFrame(rtk.points[-50:])
    map_fig = px.scatter_mapbox(df, lat='lat', lon='lon', color='fix',
                               hover_data=['time', 'alt', 'sats'],
                               mapbox_style="open-street-map",
                               title=f"RTK Survey: {len(df)} Points - {rtk.status}")
    map_fig.update_layout(height=400)
    
    # Altitude plot
    alt_fig = px.line(df, x='time', y='alt', color='fix',
                     title="Real-time Altitude (RTK Fixed = Green)")
    alt_fig.update_layout(height=300)
    
    return rtk.status, rtk.fix_type, str(rtk.sats), map_fig, alt_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
