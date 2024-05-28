from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from plotly.graph_objs import Scatter

engine = create_engine('postgresql://postgres:nah7equi@127.0.0.1:5432/Macroeconomics')
Session = sessionmaker(bind=engine)

def fetch_data(query):
    with Session() as session:
        return pd.read_sql(query, session.bind)

df_inflation = fetch_data("SELECT month, inflation_rate FROM inflation;")
df_unemployment = fetch_data("SELECT month, unemployment_rate FROM unemployment;")
df_key_rate = fetch_data("SELECT month, key_rate FROM key_rate;")

df_merged = pd.merge(df_inflation, df_unemployment, on="month")
df_merged = pd.merge(df_merged, df_key_rate, on="month")

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.RangeSlider(
            id='month-slider',
            min=0,
            max=len(df_inflation['month'].unique()) - 1,
            value=[0, len(df_inflation['month'].unique()) - 1],
            marks={i: month for i, month in enumerate(df_inflation['month'].unique())},
            step=None
        )
    ], style={'position': 'fixed', 'width': '70%', 'z-index': '999'}),
    html.Div([
        dcc.Graph(id='inflation-graph'),
        dcc.Graph(id='unemployment-graph'),
        dcc.Graph(id='phillips-curve'),
        dcc.Graph(id='key-rate'),
        dcc.Graph(id='correlation-heatmap'),
        dcc.Graph(id='scatter-matrix') 
    ], style={'padding-top': '50px'})
])

@app.callback(
    [Output('inflation-graph', 'figure'),
     Output('unemployment-graph', 'figure'),
     Output('phillips-curve', 'figure'),
     Output('key-rate', 'figure'),
     Output('correlation-heatmap', 'figure'),
     Output('scatter-matrix', 'figure')],
    [Input('month-slider', 'value')]
)

def update_graphs(slider_range):
    months = df_inflation['month'].unique()
    selected_months = months[slider_range[0]:slider_range[1]+1]
    filtered_inflation = df_inflation[df_inflation['month'].isin(selected_months)]
    filtered_unemployment = df_unemployment[df_unemployment['month'].isin(selected_months)]
    filtered_keyrate = df_key_rate[df_key_rate['month'].isin(selected_months)]
    filtered_merged = df_merged[df_merged['month'].isin(selected_months)]

    new_fig_inflation = px.line(filtered_inflation, x="month", y="inflation_rate", title="Инфляция со временем")
    new_fig_unemployment = px.line(filtered_unemployment, x="month", y="unemployment_rate", title="Уровень безработицы со временем")
    new_fig_keyrate = px.line(filtered_keyrate, x="month", y="key_rate", title="Ключевая ставка со временем")
    new_fig_phillips = px.scatter(filtered_merged, x="unemployment_rate", y="inflation_rate", title="Кривая Филлипса", hover_data={"month": True})
    coeffs = np.polyfit(filtered_merged['unemployment_rate'], filtered_merged['inflation_rate'], 2)
    x_range = np.linspace(filtered_merged['unemployment_rate'].min(), filtered_merged['unemployment_rate'].max(), 100)
    y_poly = np.polyval(coeffs, x_range)
    new_fig_phillips.add_trace(Scatter(x=x_range, y=y_poly, mode='lines', name='Кривая Филлипса', line=dict(color='red', dash='dash')))
    correlation = filtered_merged[['inflation_rate', 'unemployment_rate', 'key_rate']].corr()
    new_fig_heatmap = px.imshow(correlation, text_auto=True, aspect="auto", title="Тепловая карта корреляции")
    fig_scatter_matrix = px.scatter_matrix(
        filtered_merged,
        dimensions=['inflation_rate', 'unemployment_rate', 'key_rate'],
        title="Scatter Matrix",
        labels={'inflation_rate': 'Инфляция (%)', 'unemployment_rate': 'Безработица (%)', 'key_rate': 'Ключевая ставка (%)'},
        color_continuous_scale=px.colors.sequential.Viridis  # Использование последовательной цветовой схемы
    )

    fig_scatter_matrix.update_traces(marker=dict(size=5, opacity=0.8))

    figs1 = [new_fig_inflation, new_fig_unemployment, new_fig_keyrate, new_fig_phillips]

    for fig in figs1:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=800,
            width=1200,
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='LightGrey'),
        )
    
    figs2 = [new_fig_heatmap, fig_scatter_matrix]
    for fig in figs2:
        fig.update_layout(
            height=800,
            width=800,
        )
    return new_fig_inflation, new_fig_unemployment, new_fig_keyrate, new_fig_phillips, new_fig_heatmap, fig_scatter_matrix

if __name__ == '__main__':
    app.run_server(debug=True)
