import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

color_palette = px.colors.qualitative.Plotly

def plot_scatter(df, x, y):
    # Aggregate the data to get the number of observations for each combination of x and y values
    counts = df.groupby([x, y]).size().reset_index(name='count')
    
    # Create the scatter plot with point size based on the number of observations
    fig = px.scatter(counts, x=x, y=y, size='count',
                     title=f'Relationship between {x.capitalize()} and {y.capitalize()}',
                     labels={x: x.capitalize(), y: y.capitalize()})
    fig.update_layout(height=600)
    
    return fig

def calculate_bar_data(df):
    
    bar_data = []
    
    
    for col in df.columns:
        value_counts = df[col].value_counts(normalize=True) * 100
        for i, (value, count) in enumerate(value_counts.items()):
            color = color_palette[i % len(color_palette)]
            bar = go.Bar(
                x=[count],
                y=[col.capitalize()],
                orientation='h',
                name=value,
                marker=dict(color=color),
                text=[f"{value} {count:.1f}%"],
                textposition='inside',
                hoverinfo='x+text',
                showlegend=False
            )
            bar_data.append(bar)
    return bar_data

def plot_categorical_distribution(df, height, width):
    bar_data = calculate_bar_data(df)
    fig = go.Figure(data=bar_data)
    fig.update_layout(
        title='BAR',
        xaxis_title='Pourcentage (%)',
        yaxis_title='Colonnes',
        barmode='stack',
        height=height, 
        width = width

    )
    return fig

def calculate_statistics(df):
    # Calculate mean and max values for each column in the DataFrame
    means = df.mean().tolist()
    max_values = df.max().tolist()
    return means, max_values

def create_radar_trace(r_values, theta_values, name):
    # Create a radar trace for a given set of values
    return go.Scatterpolar(
        r=r_values,
        theta=theta_values,
        fill='toself',
        name=name
    )

def plot_radar_comparison(df, filtered_df, radar_size=(600, 600)):
    # Calculate statistics for the original DataFrame
    means_df, max_values_df = calculate_statistics(df)
    
    if filtered_df is not None:
        # Calculate statistics for the filtered DataFrame
        means_filtered, max_values_filtered = calculate_statistics(filtered_df)
    else:
        means_filtered, max_values_filtered = None, None
    
    # Get column names
    categories = df.columns.tolist()
    
    # Create radar traces for the original DataFrame
    trace_means_df = create_radar_trace(means_df, categories, 'Mean Values (Original)')
    trace_max_values_df = create_radar_trace(max_values_df, categories, 'Max Values (Original)')
    
    # Add radar traces for the filtered DataFrame if it's not None
    traces = [trace_means_df, trace_max_values_df]
    if means_filtered is not None and max_values_filtered is not None:
        trace_means_filtered = create_radar_trace(means_filtered, categories, 'Mean Values (Filtered)')
        trace_max_values_filtered = create_radar_trace(max_values_filtered, categories, 'Max Values (Filtered)')
        traces.extend([trace_means_filtered, trace_max_values_filtered])
    
    # Create a Plotly figure
    fig = go.Figure(traces)
    
    # Update layout
    max_value = max(max(max_values_df), max(max_values_filtered)) if max_values_filtered is not None else max(max_values_df)
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_value]  # Adjust the range based on the maximum values
            )),
        showlegend=True,
        width=radar_size[0],
        height=radar_size[1]
    )

    return fig

def plot_bar_comparison(df, filtered_df, bar_size=(600, 600)):
    # Calculate statistics for the original DataFrame
    means_df, max_values_df = calculate_statistics(df)
    
    if filtered_df is not None:
        # Calculate statistics for the filtered DataFrame
        means_filtered, max_values_filtered = calculate_statistics(filtered_df)
    else:
        means_filtered = max_values_filtered = None
    
    # Get column names
    categories = df.columns.tolist()
    
    # Create bar traces for the original DataFrame
    trace_means_df = go.Bar(x=categories, y=means_df, name='Mean Values (Original)')
    trace_max_values_df = go.Bar(x=categories, y=max_values_df, name='Max Values (Original)')
    
    # Add bar traces for the filtered DataFrame if it's not None
    traces = [trace_means_df, trace_max_values_df]
    if means_filtered is not None and max_values_filtered is not None:
        trace_means_filtered = go.Bar(x=categories, y=means_filtered, name='Mean Values (Filtered)')
        trace_max_values_filtered = go.Bar(x=categories, y=max_values_filtered, name='Max Values (Filtered)')
        traces.extend([trace_means_filtered, trace_max_values_filtered])
    
    # Create a Plotly figure
    fig = go.Figure(data=traces)
    
    # Update layout
    # max_value = max(max(max_values_df), max(max_values_filtered)) if max_values_filtered is not None else max(max_values_df)
    fig.update_layout(
        barmode='group',  # Group bars together
        yaxis=dict(title='Values'),  # Add title to y-axis
        showlegend=True,
        width=bar_size[0],
        height=bar_size[1]
    )

    return fig