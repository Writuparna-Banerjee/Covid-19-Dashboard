import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash import Dash
from dash.dependencies import Input,Output
from io import StringIO
import requests



# external CSS stylesheetsp
external_stylesheets = [
   {
       'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
       'rel': 'stylesheet',
       'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
       'crossorigin': 'anonymous'
   }
]


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

url="https://datahub.io/core/covid-19/r/worldwide-aggregated.csv"

s=requests.get(url, headers= headers).text

df_world=pd.read_csv(StringIO(s)) ## worldwide-cases per day

url="https://datahub.io/core/covid-19/r/countries-aggregated.csv"
s=requests.get(url, headers= headers).text

df_con=pd.read_csv(StringIO(s)) ## per country cases per day

url="https://datahub.io/core/covid-19/r/key-countries-pivoted.csv"
s=requests.get(url, headers= headers).text

df_key=pd.read_csv(StringIO(s)) ## The rising cases of key countries per day


url="https://datahub.io/core/covid-19/r/time-series-19-covid-combined.csv"
s=requests.get(url, headers= headers).text

df_t=pd.read_csv(StringIO(s)) ## time series')

a=df_world.shape[0]
Confirmed_world=df_world[['Date','Confirmed']].iloc[a-1].reset_index().iloc[1,1]
Recovered_world=df_world[['Date','Recovered']].iloc[a-1].reset_index().iloc[1,1]
Deaths_world=df_world[['Date','Deaths']].iloc[a-1].reset_index().iloc[1,1]
Increaserate_world=df_world[['Date','Increase rate']].iloc[a-1].reset_index().iloc[1,1]

trace=go.Scatter(x=df_world['Date'],y=df_world['Confirmed'],mode='lines+markers',marker={'color':'#00a65a'},name='Confirmed')
trace1=go.Scatter(x=df_world['Date'],y=df_world['Deaths'],mode='lines+markers',name='Deaths')
trace2=go.Scatter(x=df_world['Date'],y=df_world['Recovered'],mode='lines+markers',name='Recovered')
data=[trace,trace1,trace2]
layout=go.Layout(title='The rise in Covid-19 cases every day',xaxis={'title':'Date'},yaxis={'title':'Total cases'})
fig=go.Figure(data=data,layout=layout)

trace3=go.Scatter(x=df_key['Date'],y=df_key['China'],mode='lines+markers',marker={'color':'#00a65a'},name='China')
trace4=go.Scatter(x=df_key['Date'],y=df_key['US'],mode='lines+markers',name='US')
trace5=go.Scatter(x=df_key['Date'],y=df_key['United_Kingdom'],mode='lines+markers',name='United_Kingdom')
trace6=go.Scatter(x=df_key['Date'],y=df_key['Italy'],mode='lines+markers',name='Italy')
trace7=go.Scatter(x=df_key['Date'],y=df_key['France'],mode='lines+markers',name='France')
trace8=go.Scatter(x=df_key['Date'],y=df_key['Germany'],mode='lines+markers',name='Germany')
trace9=go.Scatter(x=df_key['Date'],y=df_key['Spain'],mode='lines+markers',name='Spain')
trace10=go.Scatter(x=df_key['Date'],y=df_key['Iran'],mode='lines+markers',name='Iran')
data1=[trace3,trace4,trace5,trace6,trace7,trace8,trace9,trace10]
layout=go.Layout(title='The number of confirmed cases in Key countries',xaxis={'title':'Date'},yaxis={'title':'Total cases'})
fig1=go.Figure(data=data1,layout=layout)



options=[
   {'label':'Confirmed', 'value':'Confirmed'},
   {'label':'Recovered', 'value':'Recovered'},
   {'label':'Deaths', 'value':'Deaths'},

]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server
app.layout=html.Div([
    html.H1("Corona Virus Pandemic",style={'color':'#fff','text-align':'center'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Confirmed Cases",className='text-light'),
                    html.H4(Confirmed_world,className='text-light')
                ],className='card-body')
            ],className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered",className='text-light'),
                    html.H4(Recovered_world,className='text-light')
                ],className='card-body')
            ],className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths",className='text-light'),
                    html.H4(Deaths_world,className='text-light')
                ],className='card-body')
            ],className='card bg-warning')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Increase Rate",className='text-light'),
                    html.H4(Increaserate_world,className='text-light')
                ],className='card-body')
            ],className='card bg-success')
        ], className='col-md-3')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                   dcc.Graph(id='line chart',figure=fig)
                ],className='card-body')
            ],className='card')
        ],className='col-md-6'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='line chart1',figure=fig1)
                ], className='card-body')
            ], className='card')
        ],className='col-md-6'),
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options ,value='Confirmed'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker1',options=options ,value='Confirmed'),
                    dcc.Graph(id='choropleth')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row')
],className='container')




@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(type):
    if type=='Confirmed':
        pbar=df_con.groupby('Country')['Confirmed'].max().reset_index()
        return {'data':[go.Bar(x=pbar['Country'], y=pbar['Confirmed'])],
            'layout':go.Layout(title='Confirmed cases per country')}
    elif type=='Recovered':
        pbar1 = df_con.groupby('Country')['Recovered'].max().reset_index()
        return {'data': [go.Bar(x=pbar1['Country'], y=pbar1['Recovered'])],
                'layout': go.Layout(title='Recovered cases per country')}
    else:
        pbar2 = df_con.groupby('Country')['Deaths'].max().reset_index()
        return {'data': [go.Bar(x=pbar2['Country'], y=pbar2['Deaths'])],
                'layout': go.Layout(title='Death cases per country')}

@app.callback(Output('choropleth', 'figure'), [Input('picker1', 'value')])
def update_graph(type):
    if type == 'Confirmed':
         dff = df_con.groupby('Country')['Confirmed'].max().reset_index()
         return {'data': [go.Choropleth(locations=dff['Country'], z=dff['Confirmed'],autocolorscale=False,
                                        locationmode='country names',colorscale='rainbow',
                                        marker={'line':{'color':'rgb(180,180,180)','width':0.5}},
                                        colorbar={'thickness':15,'len':1.,'x':0.9,'y':0.7,
                                        'title':{'text':'Confirmed','side':'bottom'}})],
                'layout': go.Layout(title='Confirmed cases all over the world')}
    elif type == 'Recovered':
        dff1 = df_con.groupby('Country')['Recovered'].max().reset_index()
        return {'data': [go.Choropleth(locations=dff1['Country'], z=dff1['Recovered'],autocolorscale=False,
                                        locationmode='country names',colorscale='rainbow',
                                        marker={'line':{'color':'rgb(255,255,255)','width':0.5}},
                                        colorbar={'thickness':15,'len':1,'x':0.9,'y':0.7,
                                        'title':{'text':'Recovered','side':'bottom'}})],
                 'layout': go.Layout(title='Recovered cases all over the world')}
    else:
        dff2 = df_con.groupby('Country')['Deaths'].max().reset_index()
        return {'data': [go.Choropleth(locations=dff2['Country'], z=dff2['Deaths'],autocolorscale=False,
                                        locationmode='country names',colorscale='rainbow',
                                        marker={'line':{'color':'rgb(255,255,255)','width':0.5}},
                                        colorbar={'thickness':15,'len':1,'x':0.9,'y':0.7,
                                        'title':{'text':'Deaths','side':'bottom'}})],
                'layout': go.Layout(title='Death cases all over the world')}







if __name__ == "__main__":
    app.run_server(debug=False)

