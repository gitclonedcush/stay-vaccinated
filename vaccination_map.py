import numpy as np
import pandas as pd
import plotly.graph_objects as go

pd.options.display.float_format = '{:.1f}'.format

def get_current_location_data(vaccinations, iso_code):
	location_vaccinations = vaccinations[vaccinations['iso_code'] == iso_code].sort_values(['date'], ascending=False)
	for _, row in location_vaccinations.iterrows():
		if row['people_vaccinated'] > 0:
			return row


def read_data():
	vaccinations = pd.read_csv('./vaccinations/vaccinations.csv')
	population = pd.read_csv('./population/population_totals.csv')

	colnames = ['iso_code', 'date', 'people_vaccinated', 'people_fully_vaccinated']
	vaccinations = vaccinations[colnames]

	population = population[['Country Name','Country Code', '2020']]
	population = population.rename(columns={"Country Name": "location", "Country Code": "iso_code", "2020" : "total_population"})
	population['total_population'] = population['total_population'].mul(1.01).apply(np.floor)

	vaccinations_current = pd.DataFrame(columns = colnames)
	iso_uniq = vaccinations['iso_code'].unique()
	for iso in iso_uniq:
		vaccinations_current = vaccinations_current.append(get_current_location_data(vaccinations, iso), ignore_index=True)


	vaccinations_current = pd.merge(vaccinations_current, population, on = 'iso_code')
	vaccinations_current['percent_vaccinated'] = (vaccinations_current['people_vaccinated'] / vaccinations_current['total_population']) * 100
	vaccinations_current = vaccinations_current.sort_values('iso_code')

	return vaccinations_current


def build_vaccinations_map(vaccinations_current):
	max_population = vaccinations_current['total_population'].max()
	scale = max_population / 100

	# colors = ['#fea889', '#f16a6f', '#def2f1', '#91d4d1', '#205566']
	layout = {
		'title': go.layout.Title({
			'text': 'Global Covid Vaccinations',
			'font': {
				'color': 'white'
			}
		}),
		'legend': go.layout.Legend(
			{
				'font': {
					'color': 'white'
				}
			}
		),
		'height': 1000,
		'width': 1400,
		'paper_bgcolor': 'rgba(17,17,17,1)',
		'geo': go.layout.Geo({
			'bgcolor': 'rgba(17,17,17,1)',
			'showocean': True,
			'oceancolor': 'rgba(51,153,255,0.9)',
			'showland': True,
			'landcolor': 'rgb(2,48,32,1)',
			'resolution': 50,
			'scope': 'world',
			'showframe': True,
			'showcoastlines': True,
			'showcountries': True,
			'projection_type': 'orthographic',
		}),
	}

	fig = go.Figure(layout=layout)

	for i, row in vaccinations_current.iterrows():
		fig.add_trace(go.Scattergeo(
				locationmode = 'ISO-3',
				locations = [row.iso_code],
				text = row.percent_vaccinated,
				name = row.location,
				mode = 'markers',
				marker=dict(
					size=np.log1p(row.percent_vaccinated)**2,
					sizemode='area',
				)))

	return fig
