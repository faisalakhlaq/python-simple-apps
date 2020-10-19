from pandas_datareader import data
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN


# TODO compare two stocks
class StockAnalyzer:

    def inc_dec(self, open_value, close_value):
        """
        @args open and close value of stock
        @returns stock value increase or decrease
        """
        if not open_value or not close_value:
            return "Undefined"
        if close_value > open_value:
            return "Increase"
        elif open_value > close_value:
            return "Decrease"
        else:
            return "Equal"

    def get_data(self, stock_ticker, start_date, end_date):
        """
        @:returns Stock data for the given dates
        """
        # TODO get the name of company and data source from the user and display its result
        # Provide an option to the user to get data from WorldBank (wb) and other sources.
        # For Worldbank we have to import from pandas_datareader import wb
        df = data.DataReader(name=stock_ticker, data_source="yahoo", start=start_date, end=end_date)
        # create a column status. Status values will be used in plotting the graph
        df["Status"] = [self.inc_dec(open_value=o, close_value=c)
                        for o,c in zip(df.Open, df.Close)]
        # create a coloumn middle which will be used to plot the
        # middle of the rectangle on the graph
        df["Middle"] = (df.Open+df.Close)/2
        df["Height"] = abs(df.Open-df.Close)
        return df

    def get_graph(self, stock_ticker, start_date, end_date):
        """
        @:returns A graph displaying stock data for specific dates
        """
        df = self.get_data(stock_ticker, start_date, end_date)
        p = figure(title="Stock Data Chart", x_axis_type='datetime',
                   width=800, height=250, sizing_mode="scale_width")
        # The width of the rectangle should be 12 hours as the
        # graph x-axis is plotted as date/hours
        hours_12 = 12*60*60*1000
        p.grid.grid_line_alpha = 0.5

        p.segment(df.index, df.High, df.index, df.Low, color='black')
        p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
               hours_12, df.Height[df.Status == "Increase"], fill_color="#CCFFFF",
               line_color="black")
        p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
               hours_12, df.Height[df.Status == "Decrease"], fill_color="#FF3333",
               line_color="black")
        script1, div1 = components(p)
        cdn_js = CDN.js_files[0]
        return [script1, div1, cdn_js]
