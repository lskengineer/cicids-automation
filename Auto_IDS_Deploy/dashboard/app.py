import dash
from dash import dcc, html
import pymongo
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ids_logs"]
alerts = db["alerts"]

app.layout = html.Div([
    html.H2("Live IDS Dashboard"),
    html.Div(id="alert-log"),
    dcc.Interval(id="interval-component", interval=2000, n_intervals=0)
])

@app.callback(Output("alert-log", "children"), Input("interval-component", "n_intervals"))
def update_log(n):
    latest_alerts = list(alerts.find().sort("_id", -1).limit(5))
    return html.Ul([html.Li(f"{alert['features']} - {alert['prediction']}") for alert in latest_alerts])

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
