import model
import bokeh
from bokeh.layouts import column, row
from bokeh.plotting import figure, output_file, show
from bokeh.models import Tabs, Panel
from bokeh.models.widgets import Select, RangeSlider, CheckboxGroup


class View:
    """Visualise demographical data from different years and
        different countries from a given dataset with bokeh."""

    def __init__(self, data):
        self.data = data
        self.lines = list()

    def visualise(self):
        """This function visualises our whole datatset"""
        # output to static HTML file
        output_file("index.html")

        # Make up plot
        for data_type in self.data.columns[2:]:
            self.lines.append(self._make_line(data_type))

        # Adding a selector
        countries = self.data.Country.drop_duplicates().to_list()
        select = Select(title="Displayed Country:", value=countries[0], options=countries)
        years = RangeSlider(start=1950, end=2018, value=(1964, 2001), step=1, title="Year range:")

        # show the results
        show(row(Tabs(tabs=self.lines), column(select, years)))

    def _make_line(self, interest):
        """Initialize a line for a certain demopgraphic data type."""

        # Initializing the figure
        line = figure(title=interest, x_axis_label='Year', y_axis_label=interest, width=1200)

        # Adding a line renderer with legend and line thickness
        for country in self.data['Country'].drop_duplicates():
            newdata = self.data[self.data['Country'] == country]
            x = newdata['Year']
            y = newdata[interest]
            line.line(x, y, legend_label=country, line_width=2)

        # Creating a tab for the panel
        tab = Panel(child=line, title=interest)

        return tab

