import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


# Load data
cleaned_response_times_df = pd.read_excel('cleaned_response_output.xlsx')
no_responses_df = pd.read_excel('no_response_output.xlsx')

# Load the precomputed Weighted Average Response Time data
weighted_avg_response_time_df = pd.read_excel('weighted_average_response_time.xlsx')

# Ensure the cleaned data has the correct types
cleaned_response_times_df['entry_date'] = pd.to_datetime(cleaned_response_times_df['entry_date'])
cleaned_response_times_df['earliest_entry_time'] = pd.to_datetime(cleaned_response_times_df['earliest_entry_time'])
cleaned_response_times_df['closest_response_time'] = pd.to_datetime(cleaned_response_times_df['closest_response_time'])
cleaned_response_times_df['response_time_hours'] = pd.to_numeric(cleaned_response_times_df['response_time_hours'], errors='coerce')

# Apply custom formatting function
def add_ordinal_suffix(date):
    day = date.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return f"{day}{suffix} {date.strftime('%b, %Y %H:%M')}"

cleaned_response_times_df['earliest_entry_time_formatted'] = cleaned_response_times_df['earliest_entry_time'].apply(add_ordinal_suffix)
cleaned_response_times_df['closest_response_time_formatted'] = cleaned_response_times_df['closest_response_time'].apply(add_ordinal_suffix)

# Get unique organisations and teams
organisations = cleaned_response_times_df['organisationId'].unique()

# Initialize the Dash app with Bootstrap theme and custom CSS
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/styling.css'])
server=app.server

# Add "All" to dropdown options
organisation_options = [{'label': 'All', 'value': 'All'}] + [{'label': org, 'value': org} for org in organisations]


# Define the layout using Dash Bootstrap Components
# Layout
app.layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col([
            html.H4("Clinical Analytics",className="display-4", style={'color': '#4d94ff'}),
            html.Hr(),
            html.P("Welcome to the Post Surgical Response Dashboard. This tool provides comprehensive insights into response times and team performance across post-surgical pathways.", className="lead", style={'font-size': '18px'} ),
            

            html.Label('Select Organisation:', className="mt-4"),
            dcc.Dropdown(
                id='org-dropdown',  # ID should match here
                options=organisation_options,
                value='All', 
                clearable=False,
                className="mb-3"
            ),
            
            html.Label('Select Team:'),
            dcc.Dropdown(
                id='team-dropdown',  # ID should match here
                clearable=False,
                className="mb-3"
            ),

            html.Label('Select Date Range:', className="mt-4"),
            
            # Wrap the DatePickerRange in a Div to place it on a new line
            html.Div(
                dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=cleaned_response_times_df['earliest_entry_time'].min(),
                    end_date=cleaned_response_times_df['earliest_entry_time'].max(),
                    display_format='DD/MM/YYYY',
                    className="mb-3"
                ),
                style={'margin-top': '5px'}  # Ensure the DatePickerRange is below the label with some space
            ),

                        # Adding the image after the DatePickerRange
            html.Img(
                src='/assets/open-label-extension.png',  # Path to your image in the assets folder
                style={'width': '100%', 'margin-top': '10px'}  # Adjust the width and margin as needed
            ),
        ], id='sidebar', width=3, style={'border-right': '1px solid #ccc', 'height': '100vh', 'padding': '20px'}),
        

        dbc.Col([
            dcc.Tabs(id='tabs', value='overview', children=[
                dcc.Tab(label='Overview', value='overview', children=[
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("Median Response Time", className="card-title"),
                                html.H3(id='median-response-time', className='card-text', style={'color': '#007bff'})  # ID should match here
                            ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
                        ], className="shadow-sm rounded", style={'height': '100px'})),
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("Not Responded", className="card-title"),
                                html.H3(id='no-response-percentage', className='card-text', style={'color': '#007bff'})  # ID should match here
                            ],style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
                        ], className="shadow-sm rounded", style={'height': '100px'})),
                        dbc.Col(dbc.Card([
                            dbc.CardBody([
                                html.H6("Patient Count", className="card-title"),
                                html.H3(id='patient-count', className='card-text', style={'color': '#007bff'})  # ID should match here
                            ],style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
                        ], className="shadow-sm rounded", style={'height': '100px'}))
                    ], className="mb-4", style={'margin-top': '20px'}),

                    dbc.Card([
                        dbc.CardBody([
                            html.H5("1. Response Time Analysis", className="display-4", style={'font-size': '24px'}),
                            dcc.Graph(id='response-time-graph')  # ID should match here
                        ])
                    ], className="mb-4 shadow-sm rounded", style={'margin-top': '20px'}),

                # New Card for Weighted Average Response Time by Organisation
                dbc.Card([
                    dbc.CardBody([
                        html.H5("2. Weighted Average Response Time by Organisation", className="display-4", style={'font-size': '24px'}),
                        dcc.Graph(
                            id='weighted-avg-response-time',
                            figure=px.bar(
                                weighted_avg_response_time_df,
                                x='organisationId',
                                y='weighted_avg_response_time',
                                title='Weighted Average Response Time by Organisation and Overall',
                                labels={'organisationId': 'Organisation', 'weighted_avg_response_time': 'Weighted Average Response Time (Hours)'},
                                color='weighted_avg_response_time',
                                color_continuous_scale='Blues'
                            )
                        )
                    ])
                ], className="mb-4 shadow-sm rounded", style={'margin-top': '20px'}),

                # New Card for the New Visualisation
                dbc.Card([
                    dbc.CardBody([
                        html.H5("3. Average Response Time across different teams", className="display-4", style={'font-size': '24px'}),
                        html.P("Note: Please only select organisations and not teams for this analysis."),
                        dcc.Graph(id='avg-response-time-audit-graph')  # New Graph ID
                    ])
                ], className="mb-4 shadow-sm rounded", style={'margin-top': '20px'})

                ]),
                dcc.Tab(label='Trends', value='trends', children=[
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5(" 4. Average Response Time Trend", className="display-4", style={'font-size': '24px'}),
                                    dcc.Graph(id='line-chart')
                                ])
                            ], className="mb-4 shadow-sm rounded", style={'margin-top': '20px'})
                        ], width=12)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.H5("5. Team Response Numbers Heatmap", className="display-4", style={'font-size': '24px', 'text-align': 'left'}),
                                    dcc.Graph(id='team-overlap-heatmap', style={'width': '100%', 'display': 'block', 'margin': 'auto'}) 
                                ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center'})
                            ], className="mb-4 shadow-sm rounded", style={'margin-top': '20px'})
                        ], width=12)
                    ])
                ]),
            ])
        ], width=9)
    ]),
])
# Define the team_color_map outside the function to make it accessible
color_discrete_map = px.colors.qualitative.Plotly
team_color_map = {team: color_discrete_map[i % len(color_discrete_map)] for i, team in enumerate(cleaned_response_times_df['teamId'].unique())}


# Callback to update team dropdown based on selected organisation
@app.callback(
    Output('team-dropdown', 'options'),
    Output('team-dropdown', 'value'),
    Input('org-dropdown', 'value')
)
def update_team_dropdown(selected_org):
    if selected_org == 'All':
        options = [{'label': 'All', 'value': 'All'}] + [{'label': str(team), 'value': team} for team in cleaned_response_times_df['teamId'].dropna().unique()]
    else:
        filtered_teams = cleaned_response_times_df[cleaned_response_times_df['organisationId'] == selected_org]['teamId'].dropna().unique()
        options = [{'label': 'All', 'value': 'All'}] + [{'label': str(team), 'value': team} for team in filtered_teams]

    return options, 'All'  # Ensure options is defined and returned



# Callback to update the plot and cards based on organisation and team selection
@app.callback(
    [Output('response-time-graph', 'figure'),
     Output('median-response-time', 'children'),
     Output('no-response-percentage', 'children'),
     Output('patient-count', 'children')],
    [Input('org-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_dashboard(selected_org, selected_team):
    # Filter data based on selections
    if selected_org == 'All' and selected_team == 'All':
        filtered_df = cleaned_response_times_df
    elif selected_org != 'All' and selected_team == 'All':
        filtered_df = cleaned_response_times_df[cleaned_response_times_df['organisationId'] == selected_org]
    elif selected_org == 'All' and selected_team != 'All':
        filtered_df = cleaned_response_times_df[cleaned_response_times_df['teamId'] == selected_team]
    else:
        filtered_df = cleaned_response_times_df[
            (cleaned_response_times_df['organisationId'] == selected_org) &
            (cleaned_response_times_df['teamId'] == selected_team)
        ]

    # Create the scatter plot using Plotly Graph Objects
    fig = go.Figure()

    # Add traces for each team with hover data in the desired order
    for team in filtered_df['teamId'].unique():
        team_data = filtered_df[filtered_df['teamId'] == team]

        fig.add_trace(go.Scatter(
            x=team_data['earliest_entry_time'],
            y=team_data['response_time_hours'],
            mode='markers',
            marker=dict(color=team_color_map[team]),
            name=team,
            hovertemplate=(
                "patientId=%{customdata[0]}<br>"
                "teamId=%{text}<br>"
                "organisationId=%{customdata[1]}<br>"
                "response time=%{customdata[2]}<br>"
                "earliest_entry_time=%{customdata[3]}<br>"  # Use formatted earliest entry time
                "closest_response_time=%{customdata[4]}<extra></extra>"  # Use formatted closest response time
            ),
            customdata=team_data[['patientId', 'organisationId', 'response_time_formatted', 'earliest_entry_time_formatted', 'closest_response_time_formatted']],
            text=team_data['teamId']
        ))

    # Update layout with dropdowns in plotly plot
    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        )
    )

    # Calculate metrics for the cards
    median_response_time = round(filtered_df['response_time_hours'].median(), 2)

    # Calculate unique patient count in the no response dataset
    unique_no_response_patients = no_responses_df['patientId'].nunique()

    patient_count = filtered_df['patientId'].nunique()    

    return fig, f"{median_response_time} hrs", unique_no_response_patients, patient_count

# Callback to update the new visualisation based on organisation selection
@app.callback(
    Output('avg-response-time-audit-graph', 'figure'),
    [Input('org-dropdown', 'value')]
)
def update_avg_response_time_graph(selected_org):
    # Filter data based on organisation selection
    if selected_org == 'All':
        filtered_df = cleaned_response_times_df
    else:
        filtered_df = cleaned_response_times_df[cleaned_response_times_df['organisationId'] == selected_org]

    # Calculate the average response time per audit for each team
    response_summary = (
        filtered_df
        .groupby(['organisationId', 'teamId'])
        .agg(total_response_time=('response_time_hours', 'sum'),
             num_audits=('response_time_hours', 'size'))
        .reset_index()
    )
    response_summary['avg_response_time_per_audit'] = response_summary['total_response_time'] / response_summary['num_audits']

    # Create the bar plot using Plotly Express
    fig = px.bar(
        response_summary, 
        x='teamId', 
        y='avg_response_time_per_audit',
        color='teamId',
        labels={'avg_response_time_per_audit': 'Avg Response Time per Audit (Hours)', 'teamId': 'Team'},
        title=f'Average Response Time per Audit for Teams in Organization {selected_org}'
    )

    fig.update_layout(xaxis_tickangle=-45)

    return fig

# Callback to update the line chart in the Trends tab
@app.callback(
    Output('line-chart', 'figure'),
    [Input('org-dropdown', 'value'),
     Input('team-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_line_chart(selected_org, selected_team, start_date, end_date):
    # Filter the dataframe based on the selected organisation, team, and date range
    filtered_df = cleaned_response_times_df[
        (cleaned_response_times_df['organisationId'] == selected_org) &
        (cleaned_response_times_df['teamId'] == selected_team) &
        (cleaned_response_times_df['earliest_entry_time'] >= start_date) &
        (cleaned_response_times_df['earliest_entry_time'] <= end_date)
    ]
    
    # Group by a time period (e.g., month) and calculate the average response time
    filtered_df['month_year'] = filtered_df['earliest_entry_time'].dt.to_period('M')
    aggregated_df = filtered_df.groupby('month_year').agg({'response_time_hours': 'mean'}).reset_index()
    
    # Convert the period to datetime for plotting
    aggregated_df['month_year'] = aggregated_df['month_year'].dt.to_timestamp()

    # Create the line chart using the aggregated data
    fig = px.line(
        aggregated_df,
        x='month_year',
        y='response_time_hours',
        title=f'Average Response Time Trend for {selected_team} in {selected_org}',
        labels={'response_time_hours': 'Average Response Time (Hours)', 'month_year': 'Time'}
    )
    
    return fig


@app.callback(
    Output('team-overlap-heatmap', 'figure'),
    Input('org-dropdown', 'value')
)
def update_heatmap(selected_org):
    # Create a pivot table to count occurrences of teamId in each organisation
    team_org_pivot = cleaned_response_times_df.pivot_table(index='teamId', columns='organisationId', aggfunc='size', fill_value=0)

    # Create a Plotly heatmap from the pivot table
    fig = go.Figure(data=go.Heatmap(
        z=team_org_pivot.values,
        x=team_org_pivot.columns,
        y=team_org_pivot.index,
        colorscale='Blues',
        text=team_org_pivot.values,  # Display numbers on the heatmap
        texttemplate="%{text}",  # Format for text display
        textfont={"size": 12}  # Adjust font size
    ))

    # Update layout to make the heatmap responsive and visible
    fig.update_layout(
        title='Number of Recorded Responses of Teams Across Organisations',
        xaxis_title='Organisation',
        yaxis_title='Team',
        autosize=True,  # Allow figure to resize automatically
        xaxis=dict(automargin=True),  # Automatically adjust x-axis margins
        yaxis=dict(automargin=True),  # Automatically adjust y-axis margins
        margin=dict(l=0, r=0, t=50, b=0)  # Adjust margins for better fit
    )

    return fig



# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
