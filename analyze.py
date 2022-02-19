#!/usr/bin/env python3
import pandas as pd
import us
import plotly.figure_factory as ff
import plotly.graph_objects as go

state_to_fips = us.states.mapping('name', 'fips')
state_to_abbr = us.states.mapping('name', 'abbr')

colnames = ['id', 'date', 'state', 'county',
            'addr', 'death', 'injured', 'link']
df = pd.read_csv('data/data-2022-02-15.csv', names=colnames, header=0)
injured_per_state = df[['state']].groupby(
    by=['state']).size().reset_index(name='counts')
injured_per_state['fips'] = injured_per_state['state'].apply(
    lambda name: state_to_fips[name])
injured_per_state['state_abbr'] = injured_per_state['state'].apply(
    lambda name: state_to_abbr[name])

print(injured_per_state)

fig = go.Figure(data=go.Choropleth(
    locations=injured_per_state['state_abbr'],
    z=injured_per_state['counts'].astype(float),
    locationmode='USA-states',
    colorscale='Reds',
    colorbar_title="Counts"
))

fig.add_scattergeo(
    locations=injured_per_state['state_abbr'],
    locationmode='USA-states',
    text=injured_per_state['counts'],
    mode='text',
    textfont=dict(family="sans serif", size=20))

fig.update_layout(
    title_text='USA deaths and injuries related to gun violence in the past 72 hours',
    geo_scope='usa',  # limite map scope to USA
)
fig.show()
