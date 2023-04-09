import dash
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import json
import plotly.express as px

######################################################Data##############################################################

#df = pd.read_csv('data_all.csv')
df = pd.read_excel("data.xls")

factors = ['Log GDP per capita', 'Social support', 'Healthy life expectancy at birth', 'Freedom to make life choices', 'Generosity','Perceptions of corruption']

df = df[df.year >= 2015]

df['Ranking'] = df.sort_values(by=['year', 'Life Ladder']).groupby('year').cumcount(ascending=False) + 1
country_options = [dict(label=country, value=country) for country in df['Country name'].unique()]
year_options = [dict(label=year, value=year) for year in df['year'].unique()]

df_table=df.copy()
table_left = []
table_right = [] # define an empty table_1 list outside the callback function


df['Country name'].replace(['North Macedonia'], ['Macedonia'], inplace=True)
df['Country name'].replace(['State of Palestine'], ['Palestine'], inplace=True)
df['Country name'].replace(['Tanzania'], ['United Republic of Tanzania'], inplace=True)
df['Country name'].replace(['Congo (Brazzaville)'], ['Republic of Congo'], inplace=True)
df['Country name'].replace(['Congo (Kinshasa)'], ['Democratic Republic of the Congo'], inplace=True)



######################################################Interactive Components############################################


# Load GeoJSON data
with open('countries.geojson') as f:
    data_geo = json.load(f)

# To feed the GeoJson into Plotly:
# Add the 'id' key to each feature containing the value of each countries ISO-A3 code
# Which is stored in the key 'feature['properties']['ADMIN']'

for feature in data_geo['features']:
    feature['id'] = feature['properties']['ADMIN']  # or 'ISO-A3'



#Happiest cuntry card
happy_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H6("Highest score of 2022", className="card-title"),
                dbc.CardImg(src="/assets/fin.jpeg", top=True, style={"opacity": '100%', 'width': '100%'}),
                html.H3(
                    "Finland",
                    className="card-text",
                ),
                html.P(
                    "Their happiness score was:",
                    className="card-text",
                    style={'text-align': 'center'}
                ),
                html.Span("7.27"),
            ]
        ),
    ],
    style={"width": "100%"},
)


#Sadest cuntry card
sad_card  = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H6("Lowest score of 2022", className="card-title"),
                dbc.CardImg(src="/assets/afg.png", top=True, style={"opacity": '100%','width':'100%'}),
                html.H3(
                    "Afganistan",
                    className="card-text",
                ),
                html.P(
                    "Their happiness score was:",
                    className="card-text",
                    style={'text-align':'center'}
                    ),
                html.Span("1.28"),
            ]
        ),
    ],
    style={"width": "100%"})


#Map projection
map_projection=dcc.Graph(id='choropleth-map',
    figure=go.Figure(go.Choroplethmapbox(
    geojson=data_geo,
    locations=df[df['year'] == 2022]['Country name'],
    z=df[df['year'] == 2022]['Life Ladder'],
    colorscale='Viridis',
    zmin=df['Life Ladder'].min(),
    zmax=df['Life Ladder'].max()
    )).update_layout(
    mapbox_style='carto-positron',
    mapbox_zoom=1,
    mapbox_center={'lat': 0, 'lon': 0},
    height=400, margin={"r":0,"t":0,"l":0,"b":0},
    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)'))



#Country dropdown
country_dropdown=dcc.Dropdown(
    id='country_drop',
    options=country_options,
    value=['Portugal', 'Finland', 'Afganista', 'Croatia'],
    multi=True)

#Line plot
line_plot=dcc.Graph(
    id='line_plot')


#Year dropdown
left_year=dcc.Dropdown(
        id='year_drop_left',
        options=year_options,
        value=2015,
        style = dict(
            color = '#111'
            ),
    )
#Year dropdown
right_year=dcc.Dropdown(
        id='year_drop_right',
        options=year_options,
        value=2022,
        style = dict(
            color = '#111'
            ),
    )


#left table
left_table=dash_table.DataTable(
        id='left_table',
        columns=[{"name": "Country", "id": "Country name"},
                 {"name": "Ranking", "id": "Ranking","type": "numeric","format": {"specifier": ".0f"}},
                 {"name": "Life ladder", "id": "Life Ladder","type": "numeric","format": {"specifier": ".2f"}},
                 {"name": "GDP", "id": "Log GDP per capita","type": "numeric","format": {"specifier": ".2f"}},
                 {"name": "Social support", "id": "Social support","type": "numeric","format": {"specifier": ".2f"}},
                 {"name": "Healthy life", "id": "Healthy life expectancy at birth","type": "numeric","format": {"specifier": ".0f"}},
                 {"name": "Freedom", "id": "Freedom to make life choices","type": "numeric","format": {"specifier": ".2f"}},
                 {"name": "Generosity", "id": "Generosity","type": "numeric","format": {"specifier": ".2f"}},
                 {"name": "Corruption", "id": "Perceptions of corruption","type": "numeric","format": {"specifier": ".2f"}}
                 ],
        data=table_left,  # use the empty table_1 list as the initial data
        style_header={
            'backgroundColor': '#cfd9db',
            'color': '#100015',
            'border': '1px solid #aaa',
            'font-family':'Montserrat',
            'font-size':'12px'
        },
        style_data={
            'backgroundColor': '#eee',
            'color': '#100015',
            'border': '1px solid #aaa',
            'font-family':'Montserrat',
            'font-size':'10px'
        },
    )

#right table
right_table=dash_table.DataTable(
        id='right_table',
        columns=[{"name": "Country", "id": "Country name"},
             {"name": "Ranking", "id": "Ranking", "type": "numeric", "format": {"specifier": ".0f"}},
             {"name": "Life ladder", "id": "Life Ladder", "type": "numeric", "format": {"specifier": ".2f"}},
             {"name": "GDP", "id": "Log GDP per capita", "type": "numeric","format": {"specifier": ".2f"}},
             {"name": "Social support", "id": "Social support", "type": "numeric", "format": {"specifier": ".2f"}},
             {"name": "Healthy life", "id": "Healthy life expectancy at birth", "type": "numeric","format": {"specifier": ".0f"}},
             {"name": "Freedom", "id": "Freedom to make life choices", "type": "numeric","format": {"specifier": ".2f"}},
             {"name": "Generosity", "id": "Generosity", "type": "numeric", "format": {"specifier": ".2f"}},
             {"name": "Corruption", "id": "Perceptions of corruption", "type": "numeric","format": {"specifier": ".2f"}}
             ],
        data=table_right,  # use the empty table_1 list as the initial data
        style_header={
            'backgroundColor': '#cfd9db',
            'color': '#100015',
            'border': '1px solid #aaa',
            'font-family':'Montserrat',
            'font-size':'12px'
        },
        style_data={
            'backgroundColor': '#eee',
            'color': '#100015',
            'border': '1px solid #aaa',
            'font-family':'Montserrat',
            'font-size':'10px'
        },
    )

#Factors dropdown
factor_drop=dcc.Dropdown(
        id='y-axis-dropdown',
        options=[{'label': col, 'value': col} for col in factors],
        value='Perceptions of corruption',
        style = dict(
            color = '#111'
            ),
    )


#Scater plot
scatter_left=dcc.Graph(id='scatter-left')
scatter_right=dcc.Graph(id='scatter-right')


######################################################APP##############################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([

    html.Header([
        html.H1('World happiness'),
    ]),
    html.Div([

        html.Div([
            html.H2('What determine our happiness?'),
            html.P('The happiness is an important indicator of a countrys development and success. '
                   'Using data from the Gallup World Poll (GWP) surveys, the publication, World Happiness Report, ranks countries based on six different attributes: GDP per Capita, Social Support, Healthy Life Expectancy, Freedom to Make Life Choices, Generosity, and Perception of Corruption (Helliwell et al., 2023)'
                   'In this dashboard gain a better understanding of the factors that contribute to a countrys happiness and the changes that have occurred over the years. '
                   'You can find ranking of individual countries and see their happiness score (life leader).'
                   )
            ], style={'background-color':'#eee','width':'40%','margin':'auto','border-radius':'15px','padding':'3%'}),

        html.Div([
        happy_card
        ],className='happy_card'),

        html.Div([
            sad_card
            ],className='sad_card')

        ],style={'display': 'flex', 'margin':'60px 0px 100px 0px'}),

    html.Div([

        html.H2('Life leader, 2022'),
        html.P('Life leader score of different countries around the world from year 2022'),
        html.Div([
            map_projection])
        ],style={'margin':'20px 0px 100px 0px'}),

    html.Div([
        html.H2('Life leader from 2015 to 2022'),
        html.P('On this graph you can compare the Life Ladder score trends for different countries'),
        html.Div([
         html.Div([
            html.H4('Choose countries you want to se on the graph',style={'padding':'.5%'}),
            html.P('We recommend choosing up to 5 countries so you can clearly see them on the graph',style={'padding':'1%'}),
            country_dropdown],style={'width':'24%','margin':'0 auto'}),
            html.Div([line_plot],style={'background-color':'#eee','width':'70%','margin':'auto','border-radius':'15px'})
        ],style={'display': 'flex','margin':'20px 0px 100px 0px'}),
    ]),

    html.Div([
        html.Div([html.H2('Compare two years')],className='compare'),
        html.P('In next part you will gain more insight about how factors change over the years. '),

        html.Div([
            html.Div([
                html.H4('Choose first year',style={'padding':'1px'}),
                left_year],style={'width': '45%', 'margin':'auto'}),
            html.Div([
                html.H4('Choose second year',style={'padding':'1px'}),
                right_year], style={'width': '45%', 'margin':'auto'})
        ],style={'display': 'flex','padding':'30px 0px 15px 0px','background-color':'#100015'}),
        html.Div([
            html.Div([left_table], style={'width': '45%', 'margin':'auto'}),
            html.Div([right_table], style={'width': '45%', 'margin':'auto'})
        ],style={'display': 'flex','padding':'30px 0px 85px 0px','background-color':'#100015'}),
        html.Div([
        html.H2('Scatter plot graph'),
        html.P('You can choose any of six happiness factor and see how does it effect Life leader score'),
        html.Div([
        factor_drop],style={'width':'45%', 'margin':'0px 0px 0px 32px'})]),
        html.Div([
            html.Div([
                scatter_left],style={'background-color': '#eee', 'width': '45%','margin':'auto','border-radius':'15px'}),
            html.Div([
                scatter_right], style={'background-color': '#eee', 'width': '45%','margin':'auto','border-radius':'15px'})
        ], style={'display': 'flex','padding':'30px 0px 85px 0px','background-color':'#100015'}),
        html.Div([
            html.A('https://www.kaggle.com/datasets/mathurinache/world-happiness-report'),
            html.P('Amanda França (20220708), Nevena Cukrov (20221373), Virgínia Aguiar (20220707)')
    ],className='footer')
    ],style={'background-color':'#100015','color':'#eee'}),
])

######################################################Callbacks#########################################################


#Callback for lineplot
@app.callback(
    [Output(component_id='line_plot', component_property='figure'),
     Output(component_id='left_table', component_property='data'),
     Output(component_id='right_table', component_property='data'),
     Output(component_id='scatter-left', component_property='figure'),
     Output(component_id='scatter-right', component_property='figure')
     ],


    [Input(component_id='country_drop', component_property='value'),
    Input(component_id='year_drop_left', component_property='value'),
    Input(component_id='year_drop_right', component_property='value'),
    Input(component_id='y-axis-dropdown', component_property='value')]
)
def callback_line(country_list, year_left, year_right, selected_y_axis):

    data_line = []

    data_table_left = df.copy()
    data_table_left = data_table_left[(data_table_left['year'] == year_left)]
    data_table_left = data_table_left[data_table_left['Country name'].isin(country_list)]


    data_table_right = df.copy()
    data_table_right = data_table_right[(data_table_right['year'] == year_right)]
    data_table_right = data_table_right[data_table_right['Country name'].isin(country_list)]


    data_scatter_left = data_table_left.copy()
    data_scatter_right = data_table_right.copy()


    for country in country_list:
        df_line = df.loc[(df['Country name'] == country) & (df['year'] >= 2015)]
        x_line = df_line['year']
        y_line = df_line['Life Ladder']


        data_line.append(dict(type='scatter', x=x_line, y=y_line, name=country))

    layout_line = dict(title=dict(font=dict(size=24)),
                       yaxis=dict(title='Happiness Score'), xaxis=dict(title='Years'),
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)'
                       )
    line_plot_fig = go.Figure(data=data_line, layout=layout_line)



    table_left = data_table_left.to_dict('records')


    table_right = data_table_right.to_dict('records')


    scatter_left = px.scatter(
        data_scatter_left,
        x='Life Ladder',
        y=selected_y_axis,
        color='Log GDP per capita',
        color_continuous_scale='viridis',
        hover_name='Country name',
        text='Country name'
    )
    scatter_left.update_traces(textposition='top center')
    scatter_left.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')

    scatter_right = px.scatter(
        data_scatter_right,
        x='Life Ladder',
        y=selected_y_axis,
        color='Log GDP per capita',
        color_continuous_scale='viridis',
        hover_name='Country name',
        text='Country name'
    )
    scatter_right.update_traces(textposition='top center')
    scatter_right.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor = 'rgba(0, 0, 0, 0)')


    return line_plot_fig, table_left, table_right, scatter_left, scatter_right



if __name__ == '__main__':
    app.run_server(debug=True)