# Run app by entering python3 app.py on your terminal, and access the app on http://127.0.0.1:8050/

from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('data/lead_baci_data.csv')
df = df.query("product == 260700") # 260700 is code for "Lead ores and concentrates"
max_exporter_df = df.loc[df.groupby('importer')['value'].idxmax()]

# Initialize app
app = Dash()

# App layout
app.layout = html.Div([
    html.H1("Highest Lead Exporter for Each Country", style={"textAlign": "center"}),
    dcc.RadioItems(
        options=[
            {'label': 'Quantity', 'value': 'quantity'},
            {'label': 'Value', 'value': 'value'}
        ],
        value='quantity',
        id='controls-and-radio-item',
        style={"marginBottom": "20px"}
    ),
    dcc.Graph(id="choropleth-map")
])

# Add callback to update the map
@callback(
    Output('choropleth-map', 'figure'),
    Input('controls-and-radio-item', 'value')
)

def update_map(selected_metric):
    # Create choropleth map based on the selected metric
    fig = px.choropleth(
        max_exporter_df,
        locations="exporter",
        color=selected_metric,
        hover_name="importer",
        color_continuous_scale=px.colors.sequential.Plasma
    )
    return fig

# Run app
if __name__ == "__main__":
    app.run_server(debug=True)
