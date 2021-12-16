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
	vaccinations_current['hover_text'] = 'Location: ' + vaccinations_current['location'] + '<br>Population: ' + vaccinations_current["total_population"].astype(str) + '<br>Percent Vaccinated: ' + vaccinations_current["percent_vaccinated"].astype(str)

	layout = {
		'title': go.layout.Title({
			'text': 'Global Covid Vaccination Rates',
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
		'paper_bgcolor': 'rgba(24,24,24,1)',
		'geo': go.layout.Geo({
			'bgcolor': 'rgba(24,24,24,1)',
			'showocean': True,
			'oceancolor': 'rgba(51,153,255,0.9)',
			'showland': True,
			'landcolor': 'rgb(40,40,43,1)',
			'resolution': 50,
			'scope': 'world',
			'showframe': True,
			'showcoastlines': True,
			'showcountries': True,
			'projection_type': 'orthographic',
		}),
	}
	colors = ['rgba(108,40,117,1)', 'rgba(129,92,143,1)', 'rgba(163,137,173,1)', 'rgba(202,183,201,1)', 'rgba(224,224,224,1)',
		'rgba(184,207,181,1)', 'rgba(161,203,151,1)', 'rgba(77,162,91,1)', 'rgba(19,108,53,1)', 'rgba(8,93,23,1)']

	data = [
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'] < 10]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'] < 10]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'] < 10]['hover_text'],
			name = '<10',
			mode = 'markers',
			marker=dict(
				size=10,
				sizemode='area',
				opacity=0.9,
				color = colors[1]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'].between(10, 20, inclusive='left')]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'].between(10, 20, inclusive='left')]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'].between(10, 20, inclusive='left')]['hover_text'],
			name = '10-20',
			mode = 'markers',
			marker=dict(
				size=15,
				sizemode='area',
				opacity=0.9,
				color = colors[2]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'].between(20, 30, inclusive='left')]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'].between(20, 30, inclusive='left')]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'].between(20, 30, inclusive='left')]['hover_text'],
			name = '20-30',
			mode = 'markers',
			marker=dict(
				size=20,
				sizemode='area',
				opacity=0.9,
				color = colors[3]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'].between(30, 40, inclusive='left')]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'].between(30, 40, inclusive='left')]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'].between(30, 40, inclusive='left')]['hover_text'],
			name = '30-40',
			mode = 'markers',
			marker=dict(
				size=25,
				sizemode='area',
				opacity=0.9,
				color = colors[4]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'].between(40, 50, inclusive='left')]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'].between(40, 50, inclusive='left')]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'].between(40, 50, inclusive='left')]['hover_text'],
			name = '40-50',
			mode = 'markers',
			marker=dict(
				size=30,
				sizemode='area',
				opacity=0.9,
				color = colors[5]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'].between(50, 60, inclusive='left')]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'].between(50, 60, inclusive='left')]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'].between(50, 60, inclusive='left')]['hover_text'],
			name = '50-60',
			mode = 'markers',
			marker=dict(
				size=35,
				sizemode='area',
				opacity=0.9,
				color = colors[6]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'].between(60, 70, inclusive='left')]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'].between(60, 70, inclusive='left')]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'].between(60, 70, inclusive='left')]['hover_text'],
			name = '60-70',
			mode = 'markers',
			marker=dict(
				size=40,
				sizemode='area',
				opacity=0.9,
				color = colors[6]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'].between(70, 80, inclusive='left')]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'].between(70, 80, inclusive='left')]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'].between(70, 80, inclusive='left')]['hover_text'],
			name = '70-80',
			mode = 'markers',
			marker=dict(
				size=45,
				sizemode='area',
				opacity=0.9,
				color = colors[7]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'].between(80, 90, inclusive='left')]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'].between(80, 90, inclusive='left')]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'].between(80, 90, inclusive='left')]['hover_text'],
			name = '80-90',
			mode = 'markers',
			marker=dict(
				size=50,
				sizemode='area',
				opacity=0.9,
				color = colors[8]
			)
		),
		go.Scattergeo(
			locationmode = 'ISO-3',
			locations = vaccinations_current[vaccinations_current['percent_vaccinated'] >= 90]['iso_code'],
			text = vaccinations_current[vaccinations_current['percent_vaccinated'] >= 90]['percent_vaccinated'],
			hovertext = vaccinations_current[vaccinations_current['percent_vaccinated'] >= 90]['hover_text'],
			name = '>=90',
			mode = 'markers',
			marker=dict(
				size=np.log1p(vaccinations_current[vaccinations_current['percent_vaccinated'] >= 90]['percent_vaccinated'])**2,
				sizemode='area',
				opacity=0.9,
				color = colors[9]
			)
		),
	]

	fig = go.Figure(data=data, layout=layout)

	return fig
