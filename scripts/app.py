import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://nolet7:securePassword@192.168.0.119:27017/admin?authMechanism=SCRAM-SHA-256")
db = client["ids_logs"]

def get_data():
    # Fetch SHAP Data
    shap_data = list(db.shap_explanations.find({}, {"_id": 0, "index": 1, "features": 1, "shap_values": 1}))
    shap_df = pd.DataFrame(shap_data).explode(["features", "shap_values"])
    shap_df["shap_values"] = shap_df["shap_values"].apply(lambda x: sum(x) / len(x) if isinstance(x, list) and len(x) > 0 else 0)
    shap_df["shap_avg"] = shap_df.groupby("features")["shap_values"].transform("mean")

    # Fetch LIME Data
    lime_data = list(db.lime_explanations.find({}, {"_id": 0, "index": 1, "features": 1, "lime_explanation": 1}))
    lime_df = pd.DataFrame(lime_data).explode("features").explode("lime_explanation")
    lime_df[["lime_rule", "lime_value"]] = pd.DataFrame(lime_df["lime_explanation"].tolist(), index=lime_df.index)
    lime_df = lime_df.drop(columns=["lime_explanation"])
    lime_df["features"] = lime_df["features"].astype(str)  # Convert features to string for hashing
    lime_df["lime_avg"] = lime_df.groupby("features")["lime_value"].transform("mean")

    # Fetch Logs Data
    logs_data = list(db.logs.find({}, {"_id": 0, "index": 1, "log": 1}))
    logs_df = pd.DataFrame(logs_data)
    if not logs_df.empty:
        logs_df["count"] = 1  # Assign numerical value for visualization
    
    return shap_df, lime_df, logs_df

# Load Data
shap_df, lime_df, logs_df = get_data()

# Create Figures
fig_shap = px.scatter(shap_df, x="features", y="shap_values", title="SHAP Feature Importance", color="shap_values")
fig_lime = px.bar(lime_df, x="features", y="lime_value", title="LIME Feature Importance", color="lime_value")
fig_logs = px.bar(
    logs_df,
    x="index",
    y="count",  # Use count as Y-axis
    text="log",
    title="IDS Logs"
)

# Initialize Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("SHAP & LIME Analysis Dashboard"),
    html.Div([
        html.H3("SHAP Analysis"),
        dcc.Graph(figure=fig_shap)
    ]),
    html.Div([
        html.H3("LIME Analysis"),
        dcc.Graph(figure=fig_lime)
    ]),
    html.Div([
        html.H3("IDS Logs"),
        dcc.Graph(figure=fig_logs)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8060)

