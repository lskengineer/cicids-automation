#!/usr/bin/env python3

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import os

# Load processed dataset for visualization
data_file = "data/processed_ids_data.csv"
if os.path.exists(data_file):
    df = pd.read_csv(data_file)
    feature_column = df.columns[0]  # Use the first column for plotting
else:
    df = None
    feature_column = None

# Create a sample distribution plot if data is available
if df is not None:
    fig = px.histogram(df, x=feature_column, title=f"Distribution of {feature_column}")
else:
    fig = None

# SHAP and LIME plot paths
shap_plot_path = "shap_summary_plot.png"
lime_plot_path = "lime_explanation.png"

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(children=[
    html.H1("CICIDS AI Model Dashboard", style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div([
        html.H2("Feature Distribution"),
        dcc.Graph(figure=fig) if fig else html.P("❌ No dataset available for visualization."),
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H2("SHAP Explanation"),
        html.Img(src=app.get_asset_url(shap_plot_path), style={"width": "60%"}) if os.path.exists(f"assets/{shap_plot_path}") else html.P("❌ SHAP plot not found."),
        html.P("SHAP explains how features influence AI model decisions."),
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H2("LIME Explanation"),
        html.Img(src=app.get_asset_url(lime_plot_path), style={"width": "60%"}) if os.path.exists(f"assets/{lime_plot_path}") else html.P("❌ LIME plot not found."),
        html.P("LIME provides feature-level explainability for individual predictions."),
    ], style={"marginBottom": "40px"}),

    html.Div([
        html.H2("Real-time IDS Log Monitoring (Placeholder)"),
        html.P("Future updates will display IDS logs in real-time."),
    ], style={"marginBottom": "40px"}),

], style={"padding": "20px", "fontFamily": "Arial, sans-serif"})

# Run Dash app
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8060)

