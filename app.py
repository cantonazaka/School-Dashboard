import pandas as pd
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import visualizations
from data_processing import *

# Read data
filepath = r'exercice_data.csv'
df = read_data(filepath)

# Numerical columns (excluding 'StudentID')
numerical_columns_df , numerical_columns_filtered_df , other_numerical_columns_filtered_df = get_numerical_data(df)
numerical_features = numerical_columns_df.columns
# Categorical columns dataframe (excluding 'FirstName' and 'FamilyName' )
object_columns_df = get_categorical_data(df)



# Define the Dash app
app = dash.Dash(__name__)
server = app.server

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Student Prioritization Dashboard", style={'textAlign': 'center'}),
    html.Div([
    html.P("Choose the indicator:"),
    dcc.Dropdown(
        id='y-dropdown',
        options=[{'label': col.capitalize(), 'value': col} for col in numerical_features],
        value=numerical_features[0],  # Set the default value to the first numerical column
        clearable=False,   # Disable the option to clear the dropdown
        style={'width': '55%'}  # Adjust the width of the Dropdown
    ),
    html.Div([
        html.Label('Final Grade:', style={'margin-right': '10px'}),
        html.Div(
            dcc.RangeSlider(
                id='grade-slider',
                min=df['FinalGrade'].min(),
                max=df['FinalGrade'].max(),
                step=1,
                marks={i: str(i) for i in range(df['FinalGrade'].min(), df['FinalGrade'].max() + 1)},
                value=[df['FinalGrade'].min(), df['FinalGrade'].max()]
            ),
            style={'width': '80%'}  # Adjust the width of the RangeSlider
        )
    ], style={'display': 'flex', 'align-items': 'center', 'justify-content': 'flex-end', 'width': '30%'})
    ]   , style={'display': 'flex', 'justify-content': 'space-between'}), 

    html.Div(style={'display': 'flex'}, children=[
        html.Div(id='scatter-container', style={'width': '40%', 'display': 'inline-block'}, children=[
            dcc.Graph(id='scatter-plot')
        ]),

        html.Div(id='selectedbarplot-container', style={'width': '25%', 'display': 'inline-block'}, children=[
            # Add your additional visualization here (e.g., another dcc.Graph)
            dcc.Graph(id='selectedbar-plot' )
        ]),
        
        html.Div(id='allbarplot-container', style={'width': '30%', 'display': 'inline-block'}, children=[
            # Add your additional visualization here (e.g., another dcc.Graph)
            dcc.Graph(id='allbar-plot')
        ]),
    ]),

    html.Div(style={'display': 'flex'}, children=[
        html.Div(id='table-container', style={'width': '40%', 'overflowY': 'scroll'}, children=[
            dash_table.DataTable(id='datatable')
        ]),

        html.Div(id='radar-container', style={'width': '25%', 'display': 'inline-block'}, children=[
            # Add your additional visualization here (e.g., another dcc.Graph)
            dcc.Graph(id='radar-plot' )
        ]),
        html.Div(id='numericalbar-container', style={'width': '30%', 'display': 'inline-block'}, children=[
            # Add your additional visualization here (e.g., another dcc.Graph)
            dcc.Graph(id='numericalbar-plot' )
        ])
    ])
])




# Callback to update the scatter plot based on user input (dropdown value) and slicer (grade-slider) value
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('y-dropdown', 'value'),
     Input('grade-slider', 'value')]
)
def update_scatter_plot(y, grade_range):
    # Filter DataFrame based on slicer (grade-slider) values
    filtered_df = df[(df['FinalGrade'] >= grade_range[0]) & (df['FinalGrade'] <= grade_range[1])]
    
    # Call the plot_scatter function from visualizations.py with the filtered DataFrame and selected y column
    fig = visualizations.plot_scatter(filtered_df, x='FinalGrade', y=y)
    return fig

# Callback to update the table based on selected points in the scatter plot
@app.callback(
    [Output('datatable', 'data'),
     Output('selectedbar-plot', 'figure'),
     Output('radar-plot', 'figure'),
     Output('numericalbar-plot', 'figure')],  
    [Input('scatter-plot', 'clickData'),
     Input('grade-slider', 'value')],  
    [State('y-dropdown', 'value')]  
)
def update_table_and_plots(clickData, grade_range, y):
    if clickData is None:
        # Filter the dataframe with the selected range
        filtered_df = df[(df['FinalGrade'] >= grade_range[0]) & (df['FinalGrade'] <= grade_range[1])]
        
        # Get filtered numerical data for the radar plot
        _ , numerical_columns_filtered_df , other_numerical_columns_filtered_df = get_numerical_data(filtered_df)
        # Plot radar for the selected range
        radar_plot_figure = visualizations.plot_radar_comparison(numerical_columns_filtered_df, None, radar_size=(500, 600))
        # Plot vertical bar for the selected range 
        vertical_plot_figure = visualizations.plot_bar_comparison(other_numerical_columns_filtered_df, None, bar_size=(600, 600))
    else:
        # Filter the dataframe with the selected range
        filtered_slicer_df = df[(df['FinalGrade'] >= grade_range[0]) & (df['FinalGrade'] <= grade_range[1])]
        # Get filtered numerical data for the radar plot with the selected range
        _ , filtered_slicer_numerical_columns_df, other_filtered_slicer_numerical_columns_df = get_numerical_data(filtered_slicer_df)
        
        # Get the selected point
        selected_point = clickData['points'][0]
        # Filter the dataframe with the selected point
        filtered_df = df[(df['FinalGrade'] == selected_point['x']) & (df[y] == selected_point['y'])]
        # Get filtered numerical data for the radar plot with the selected point
        __, filtered_numerical_columns_df,  other_filtered_numerical_columns_df= get_numerical_data(filtered_df)
        # Plot radar for the selected range and point
        radar_plot_figure = visualizations.plot_radar_comparison(filtered_slicer_numerical_columns_df, filtered_numerical_columns_df, radar_size=(500, 600))
        # Plot vertical bar for the selected range 
        vertical_plot_figure = visualizations.plot_bar_comparison(other_filtered_slicer_numerical_columns_df, other_filtered_numerical_columns_df, bar_size=(600, 600))
    
    # Update selectedbar-plot with the new filtered DataFrame
    object_columns_filtered_df = get_categorical_data(filtered_df)
    # Set plot title
    title  = "Selected student(s)"
    selected_bar_figure = visualizations.plot_categorical_distribution(object_columns_filtered_df, title,  600, 500)
    
    return filtered_df.to_dict('records'), selected_bar_figure, radar_plot_figure , vertical_plot_figure


# Callback to update allbar-plot based on slicer (grade-slider) value
@app.callback(
    Output('allbar-plot', 'figure'),
    [Input('grade-slider', 'value')]
)
def update_allbar_plot(grade_range):
    # Set plot title
    title  = "All students"
    # Filter DataFrame based on slicer (grade-slider) values
    filtered_df = df[(df['FinalGrade'] >= grade_range[0]) & (df['FinalGrade'] <= grade_range[1])]
    
    # Plot the categorical distribution for the filtered DataFrame
    object_columns_filtered_df = get_categorical_data(filtered_df)
    all_bar_figure = visualizations.plot_categorical_distribution(object_columns_filtered_df, title ,  600, 700)
    
    return all_bar_figure

# Run the Dash app
if __name__ == '__main__':
    app.run_server(port=8080,debug=False)

