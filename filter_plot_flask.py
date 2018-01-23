import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans



# Google Maps Geo-plot API
from bokeh.models import (
   GMapPlot, GMapOptions, ColumnDataSource, Circle, Range1d, PanTool, WheelZoomTool, HoverTool, BoxSelectTool
 )
from bokeh.io import output_file, show, output_notebook
from bokeh.plotting import figure, output_file



import warnings
warnings.filterwarnings('ignore')


def create_size_column(data):
    df_fips = data.groupby('FIPS_geoID')[['priority']].count().reset_index()
    df2 = pd.merge(data,df_fips,how='left',on='FIPS_geoID')
    df2 = df2.rename(columns={'priority_y':'Count_per_FIPS'})
    df2['Normalized_count'] = df2['Count_per_FIPS']/df2['Count_per_FIPS'].max().astype(np.float64)
    sol = []
    for val in df2['Normalized_count']:
        if val <= .11:
            sol.append(2)
        else:
            sol.append(val*28)
    df2['size'] = sol
    return df2


def filter_df(data, day, hour):
    """This function takes a dataframe and returns a data frame with only:
       - Day of week
       - Hour of day
       - Lat
       - Long
       - Count_per_FIPS
       - Size column

       Inputs:
       - Dataframe
       - Day in string format
       - Hour in int format

       Output: A dataframe of:
       - Lats
       - Longs
       - Filtered based on the hour and the day put into the function
       - Count of Lats, Longs
       - Size column for plotting
       """
    # Filter columns
    col_lst = ['Day_of_week (name)', 'Hour', 'Lat', 'Long', 'FIPS_geoID', 'priority']
    lst = []
    for columns in data.columns:
        if columns in col_lst:
            lst.append(columns)

    new_df = data[lst]

    # Filter rows by Day value
    new_df = new_df[new_df['Day_of_week (name)'] == day]
    # print(new_df['Day_of_week (name)'].nunique())

    # Filter rows by Hour value
    print(type(hour))
    new_df = new_df[new_df['Hour'] == int(hour)]
    # print(new_df['Hour'].nunique())

    # Drop NaN rows
    new_df = new_df.dropna()

    # Apply 'create_size_column' function that will count incident occurences for filtered df
    new_df = create_size_column(new_df)

    return new_df[['FIPS_geoID', 'Lat', 'Long', 'Count_per_FIPS', 'size']]



def plot_df(data, day, hour, num_centroids):
    """This function takes a dataframe and plots the centroids vs the Lats, Longs of the incident data-points

       Inputs:
       - Dataframe
       - Day in string format
       - Hour in int format
       - Number of centroids wanted

       Output: A plot of lats and longs, overlayed on a map of Austin,
               filtered based on the hour and the day put into the function
    """

    # Using the function created before, applying the proper format to the dataframe for modeling
    new_df = filter_df(data, day, hour)

    # Create a dataframe that has one count per FIPS_geoID
    # This will be used for the hover tool so that only one total count is shown when one hovers
    # Includes Lat, Long, count, size
    df_count = new_df.groupby(['FIPS_geoID', 'Lat', 'Long', 'size'])['Count_per_FIPS'].count() \
        .reset_index(name='count').sort_values('count')

    # Modeling the data with KMeans
    X = np.array(new_df[['Lat', 'Long']])
    model = KMeans(n_init=100, n_clusters=int(num_centroids), max_iter=400, tol=1e-8)
    model.fit(X)
    centroids = model.cluster_centers_

    # Defining the Lat,Long to pass into Google maps API
    cent_lats = list(centroids[:, 0])
    cent_longs = list(centroids[:, 1])

    # Actual Lat,Long of incidents
    incident_lats = list(df_count['Lat'])
    incident_longs = list(df_count['Long'])

    # Normalized FIPS count to alter plot point size based on count of incidents
    # df_size = new_df['size'].values




    # Geoplotting!!!!!!!!
    map_options = GMapOptions(lat=30.2672, lng=-97.7431, map_type="roadmap", zoom=11)

    plot = GMapPlot(
        x_range=Range1d(), y_range=Range1d(), map_options=map_options)
    plot.title.text = "Austin (Day: {}, Hour: {})".format(day, hour)

    # For GMaps to function, Google requires you obtain and enable an API key:
    #
    # https://developers.google.com/maps/documentation/javascript/get-api-key
    #
    # Replace the value below with your personal API key:
    plot.api_key = os.environ['GOOGLE_API_KEY']

    completed_source = ColumnDataSource(data=dict(
        lat=cent_lats,
        lon=cent_longs, ))
    completed_dots = Circle(x="lon", y="lat", size=55, fill_color="blue", fill_alpha=0.2, line_color=None)
    plot.add_glyph(completed_source, completed_dots)

    completed_source = ColumnDataSource(data=dict(
        lat=incident_lats,
        lon=incident_longs,
        size=df_count['size'].values,
        count=df_count['count'].values))

    # Size of lat,long plots will be determind from the normalized count column
    # If size < .11 then the plot will be size=2 ... otherwise it will multiply by 28

    completed_dots = Circle(x="lon", y="lat", size="size", fill_color="red", fill_alpha=0.8, line_color=None)
    plot.add_glyph(completed_source, completed_dots)

    # Hover tool implementation
    hover = HoverTool(tooltips=[
        ("Incident Count", "@count")])

    # The P variables below are changing the location of my centroids, not sure what's going on here
    # p = figure(plot_width=200, plot_height=200, tools=[hover],title="Mouse over the dots")

    # p.circle('lon', 'lat', size=5, source=completed_source)

    # show(p)


    plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool(), hover)
    return plot