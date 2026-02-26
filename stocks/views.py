import json
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
from django.shortcuts import render
from .utils import get_stock_data

def index(request):
    stock_code = request.GET.get('code', '')
    context = {'code': stock_code}

    if stock_code:
        stock, error = get_stock_data(stock_code)
        if error:
            context['error'] = error
        else:
            monthly_data = stock.monthly_data.all().order_by('date')

            dates = [d.date.strftime('%Y-%m') for d in monthly_data]
            yields = [d.dividend_yield for d in monthly_data]
            prices = [d.closing_price for d in monthly_data]

            # Create Plotly figure
            fig = go.Figure()

            # Bar chart for dividend yield
            fig.add_trace(go.Bar(
                x=dates,
                y=yields,
                name='配当利回り (%)',
                yaxis='y1',
                marker_color='rgba(100, 149, 237, 0.7)'
            ))

            # Line chart for stock price
            fig.add_trace(go.Scatter(
                x=dates,
                y=prices,
                name='株価 (月末終値)',
                yaxis='y2',
                line=dict(color='orange', width=2)
            ))

            # Layout
            fig.update_layout(
                title=dict(
                    text=f"{stock.name} ({stock.code})",
                    font=dict(size=20),
                    x=0.5
                ),
                xaxis=dict(title='年月'),
                yaxis=dict(
                    title='配当利回り (%)',
                    side='left',
                    showgrid=False,
                    tickformat='.2f'
                ),
                yaxis2=dict(
                    title='株価',
                    side='right',
                    overlaying='y',
                    showgrid=True,
                    gridcolor='rgba(255, 255, 255, 0.1)'
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                template='plotly_dark',
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified',
                margin=dict(l=50, r=50, t=100, b=50),
            )

            graph_json = json.dumps(fig, cls=PlotlyJSONEncoder)
            context['graph_json'] = graph_json
            context['stock'] = stock

    return render(request, 'stocks/index.html', context)
