import dash

from dash import html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
	html.P("Stay Vaccinated out There!")
])


if __name__ == '__main__':
    app.run_server(debug=True)
