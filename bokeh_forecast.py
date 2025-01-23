from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource
import os

def create_bokeh_plots(df, item_id, future_months, predicted_demand):
    item_data = df[df['item_id'] == item_id].copy()
    item_data['year_month'] = item_data['transaction_date'].dt.to_period('M')
    actual_demand = item_data.groupby('year_month')['quantity'].sum().reset_index()
    actual_source = ColumnDataSource(data=dict(
        month=actual_demand['year_month'].dt.to_timestamp(),
        quantity=actual_demand['quantity']
    ))
    predicted_source = ColumnDataSource(data=dict(
        month=future_months,
        quantity=predicted_demand
    ))
    actual_plot = figure(
        title=f'Actual Demand for Item ID {item_id}',
        x_axis_label='Date',
        y_axis_label='Quantity',
        x_axis_type='datetime',
        width=800,
        height=400,
        toolbar_location='above',
        background_fill_color='#f9f9f9'
    )
    actual_plot.line(
        'month', 'quantity',
        source=actual_source,
        line_width=2,
        color='blue',
        legend_label='Actual Demand'
    )
    actual_plot.scatter(
        'month', 'quantity',
        source=actual_source,
        size=8,
        color='blue'
    )
    predicted_plot = figure(
        title=f'Predicted Demand for Item ID {item_id}',
        x_axis_label='Date',
        y_axis_label='Quantity',
        x_axis_type='datetime',
        width=800,
        height=400,
        toolbar_location='above',
        background_fill_color='#f9f9f9'
    )
    predicted_plot.line(
        'month', 'quantity',
        source=predicted_source,
        line_width=2,
        color='orange',
        legend_label='Predicted Demand'
    )
    predicted_plot.scatter(
        'month', 'quantity',
        source=predicted_source,
        size=8,
        color='orange'
    )
    plot_filename = f"uploads/demand_forecast_{item_id}.html"
    os.makedirs(os.path.dirname(plot_filename), exist_ok=True)
    output_file(plot_filename)
    save(column(actual_plot, predicted_plot))
    return plot_filename
