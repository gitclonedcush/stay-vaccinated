import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from vaccination_map import read_data, build_vaccinations_map

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

vaccinations_current = read_data()
vaccination_map = build_vaccinations_map(vaccinations_current)

header = dbc.Col(
    html.Div(
        [
            html.H2("Covid Vaccination Rates by Country", className="text-white display-3"),
            html.Hr(className="my-2"),
            html.P(
                "Author: Daniel Cushing"
            ),
        ],
        className="h-80 p-5 text-white bg-dark rounded-3",
    ),
)

app.layout = html.Div(children=[
	dbc.Row(
		header,
		class_name='bg-dark',
		style={ 'marginBottom': '2rem' }
	),
	dbc.Row(
		dbc.Col(
			dcc.Graph(figure=vaccination_map),
			width='auto'
		),
		justify='center'
	)
])


if __name__ == '__main__':
    app.run_server(debug=True)
