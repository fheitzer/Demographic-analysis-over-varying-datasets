import model
import bokeh
from bokeh.layouts import column, row
from bokeh.plotting import figure, output_file, show
from bokeh.models import Tabs, Panel
from bokeh.models.widgets import Select, RangeSlider, CheckboxGroup


def visualise(data):
    """This function visualises our whole datatset"""
    # output to static HTML file
    output_file("index.html")

    population = make_line('Population', data)
    births = make_line('Births', data)
    deaths = make_line('Deaths', data)
    immigration = make_line('Immigration', data)
    emigration = make_line('Emigration', data)

    # show the results
    show(Tabs(tabs=[population, births, deaths, immigration, emigration]))


def make_line(interest, data):
    """Initialize a line for a certain demopgraphic data type."""

    # Initializing the figure
    line = figure(title=interest, x_axis_label='Year', y_axis_label=interest, width=1200)

    # Adding a line renderer with legend and line thickness
    for country in data['Country'].drop_duplicates():
        newdata = data[data['Country'] == country]
        x = newdata['Year']
        y = newdata[interest]
        line.line(x, y, legend_label=country, line_width=2)

    # Creating a tab for the panel
    tab = Panel(child=line, title=interest)

    return tab



if __name__ == "__main__":
    data = model.merge_datasets()
    visualise(data)

