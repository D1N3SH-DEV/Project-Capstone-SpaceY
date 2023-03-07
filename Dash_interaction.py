#Coded on local IDE, not on cloud due to technical issues.

import pandas as pd
import dash
from dash import html as html
from dash import dcc as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update


spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()


app = dash.Dash(__name__)


#Creating an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                #TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                     {'label': 'All Sites', 'value': 'ALL'},
                                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                     ],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             ),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),

                                #TASK 3: Adding a range slider to select Payload
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload]
                                                ),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

#TASK 2: Adding a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(user_choice):
    spacex_df_new = spacex_df
    if user_choice == 'ALL':
        fig = px.pie(spacex_df_new, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        spacex_df_new=spacex_df[spacex_df['Launch Site']== user_choice]
        spacex_df_new=spacex_df_new.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(spacex_df_new,values='class count',names='class',title=f"Total Success Launches for site {user_choice} ")
        return fig

#TASK 4: Adding a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def scatter(user_choice,payload):
    spacex_df_filter = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]

    if user_choice=='ALL':
        fig=px.scatter(spacex_df_filter,x='Payload Mass (kg)',y='class',color='Booster Version Category',title="Correlation between Payload and Success for all Sites")
        return fig
    else:
        fig=px.scatter(spacex_df_filter[spacex_df_filter['Launch Site']==user_choice],x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Correlation between Payload and Success for {user_choice}")
        return fig

#Deploy the application
if __name__ == '__main__':
    app.run_server()