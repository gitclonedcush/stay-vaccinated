import dash
from dash import html, dcc

from vaccination_map import read_data, build_vaccinations_map

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

vaccinations_current = read_data()
vaccination_map = build_vaccinations_map(vaccinations_current)


app.layout = html.Div(children=[
	dcc.Graph(figure=vaccination_map)
])


if __name__ == '__main__':
    app.run_server(debug=True)
