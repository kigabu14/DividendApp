# visualization.py

import plotly.graph_objects as go
from config import THEME

def plot_portfolio_pie(portfolio_df):
    labels = portfolio_df['symbol']
    values = portfolio_df['market_value']
    colors = THEME['pie_colors']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+value',
        texttemplate='%{label}<br>฿%{value:,.2f}',
        insidetextorientation='radial',
        hoverinfo='label+percent'
    )])

    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor=THEME['background_color'],
        font_color=THEME['text_color'],
        showlegend=False
    )

    return fig

def plot_dividend_progress(total_dividend, goal=50000):
    percentage = min((total_dividend / goal) * 100, 100)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=total_dividend,
        delta={'reference': goal, 'increasing': {'color': THEME['accent_color']}},
        gauge={
            'axis': {'range': [0, goal]},
            'bar': {'color': THEME['accent_color']},
            'steps': [
                {'range': [0, goal * 0.5], 'color': "#444"},
                {'range': [goal * 0.5, goal], 'color': "#888"},
            ],
        },
        title={'text': f"เงินปันผลสะสม ({percentage:.2f}%)"}
    ))

    fig.update_layout(
        paper_bgcolor=THEME['background_color'],
        font_color=THEME['text_color'],
        margin=dict(t=0, b=0, l=0, r=0),
    )

    return fig
