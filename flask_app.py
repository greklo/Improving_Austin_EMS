from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import os

# Google Maps Geo-plot API
from bokeh.io import output_file, show, output_notebook
from bokeh.plotting import figure, output_file
from bokeh.embed import file_html
from bokeh.resources import CDN

# Function I created to format df to pass into model
from filter_plot_flask import plot_df

app = Flask(__name__)


# Load dataset
df = pd.read_csv("meat_and_potatoes/Data/updated_merged_df")
day_of_week=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday","Sunday"]
hour_of_day = list(range(0,24))
centroid_count = list(range(1,16))
#feature_names = iris_df.columns[0:-1].values.tolist()



# Index page, no args
@app.route('/', methods=["GET"])
def index():
	# Determine the selected feature
	day_chosen = request.args.get("day_of_week")
	if day_chosen == None:
		day_chosen = "Monday"
	hour_chosen = request.args.get("hour_of_day")

	if hour_chosen == None:
		hour_chosen = 12
	centroids_chosen = request.args.get("centroid_count")

	if centroids_chosen  == None:
		centroids_chosen = 10


	# Create the plot
	#print(day_chosen, '   ', hour_chosen,'  ',centroids_chosen)
	plot = plot_df(df, day_chosen, hour_chosen, centroids_chosen)

	# Embed plot into HTML via Flask Render
	html = file_html(plot, CDN)
	return render_template("index.html", script=html,
						   day_of_week=day_of_week,
						   hour_of_day=hour_of_day,
						   centroid_count=centroid_count)


@app.route('/submit', methods=["POST"])
def submit():
	d = request.form
	day_chosen = d["day_of_week"]
	hour_chosen = d["hour_of_day"]
	centroids_chosen = d["centroid_count"]

	plot = plot_df(df, day_chosen, hour_chosen, centroids_chosen)

	# Embed plot into HTML via Flask Render
	html = file_html(plot,CDN)

	return render_template("index.html", script=html,
						   day_of_week=day_of_week,
						   hour_of_day=hour_of_day,
						   centroid_count=centroid_count)



# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
	app.run(port=8080, debug=True)