# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                        id='site-dropdown',
                                        options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        ],
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                        ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]),
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches by Site')
        return fig
    else:
        if entered_site == 'CCAFS LC-40':
            df2 = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']

            labels = df2['class'].value_counts().index
            values = df2['class'].value_counts().values

            fig = px.pie(df2, values = values, 
            names= labels, 
            title='Total Successful Launches for CCAFS LC-40')
            return fig
        elif entered_site == 'VAFB SLC-4E':
            df2 = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
            labels = df2['class'].value_counts().index
            values = df2['class'].value_counts().values

            fig = px.pie(df2, values = values, 
            names= labels, 
            title='Total Successful Launches for VAFB SLC-4E')
            return fig
        elif entered_site == 'KSC LC-39A':
            df2 = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
            labels = df2['class'].value_counts().index
            values = df2['class'].value_counts().values

            fig = px.pie(df2, values = values, 
            names= labels, 
            title='Total Successful Launches for KSC LC-39A')
            return fig
        else:
            df2 = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
            labels = df2['class'].value_counts().index
            values = df2['class'].value_counts().values

            fig = px.pie(df2, values = values, 
            names= labels, 
            title='Total Successful Launches for CCAFS SLC-40')
 
            return [dcc.Graph(figure=fig)]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
			  Input(component_id='payload-slider', component_property='value')])
#def get_scatter_chart(entered_site, payload-slider):
def get_scatter_chart(entered_site, payload_slider):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        scat_fig = px.scatter(filtered_df, y= "class", x="Payload Mass (kg)",
        color="Booster Version Category", 
        title = "Correlation between Payload Mass and Success for all Sites")
        return scat_fig
    else:
        if entered_site == 'CCAFS LC-40':
            df2 = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
            scat_fig = px.scatter(df2, y= "class", x="Payload Mass (kg)",
            color="Booster Version Category", 
            title = "Correlation between Payload Mass and Success for CCAFS LC-40")
            return scat_fig
        elif entered_site == 'VAFB SLC-4E':
            df2 = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
            scat_fig = px.scatter(df2, y= "class", x="Payload Mass (kg)",
            color="Booster Version Category", 
            title = "Correlation between Payload Mass and Success for VAFB SLC-4E")
            return scat_fig
        elif entered_site == 'KSC LC-39A':
            df2 = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
            scat_fig = px.scatter(df2, y= "class", x="Payload Mass (kg)",
            color="Booster Version Category", 
            title = "Correlation between Payload Mass and Success for KSC LC-39A")
            return scat_fig
        else:
            df2 = spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
            scat_fig = px.scatter(df2, y= "class", x="Payload Mass (kg)",
            color="Booster Version Category", 
            title = "Correlation between Payload Mass and Success for CCAFS SLC-40")
            return scat_fig
        return [dcc.Graph(figure=scat_fig)]
# Run the app
if __name__ == '__main__':
    app.run_server()