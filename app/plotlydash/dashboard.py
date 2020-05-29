"""Create a Dash app within a Flask app."""
import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np
# from templates.layout import html_layout


def create_dashboard(server):
    """Create a Dash app."""
    dash_app = dash.Dash(server=server,
                         routes_pathname_prefix='/dashapp/',
                         external_stylesheets=['/static/css/styles.css']
                         )

    # Prepare a DataFrame
    df_table = pd.read_csv('app/data/cannabis_db.csv')
    df_histogram = pd.read_csv('app/data/strain_profile_count.csv')

    # Custom HTML layout
    # dash_app.index_string = html_layout

    # Create Layout
    dash_app.layout = html.Div(
        children=[dcc.Graph(
            id='histogram-graph',
            figure={
                'data': [
                    {
                        'x': df_histogram['profile'],
                        'y': df_histogram['count'],
                        'customdata': df_histogram['type'],
                        'name': 'Strain profile',
                        'type': 'bar',
                        'marker_color': 'indianred'
                    }],
                'marker': [
                    {
                        'color': df_histogram['type']
                    }
                ],
                'layout': {
                    'title': 'Strain Profile',
                    'height': 900,
                    'padding': 200
                }
            }),
            create_data_table(df_table)
            ],
        id='dash-container'
    )
    return dash_app.server

def create_data_table(df_table):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        data=df_table.to_dict('records'),
        columns=[{"strain_index": i, "id": i} for i in df_table.columns],
        style_as_list_view=True,
        style_cell={'padding': '5px',
                    'textAlign': 'left'
        },
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    )
    
    return table

    # table = dash_table.DataTable(
    #     id='database-table',
    #     columns=[{"strain_index": i, "id": i} for i in df.columns],
    #     data=df.to_dict('records'),
    #     sort_action="native",
    #     sort_mode='native',
    #     page_size=300
    # )