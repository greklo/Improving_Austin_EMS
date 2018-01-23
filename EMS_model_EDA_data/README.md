# EMS_Demand_Prediction_Capstone


## Overview

In the City of Austin alone, there are over one-hundred thousand EMS dispatches per year (and every year that number is
increasing). In a number of these scenarios a matter of minutes could be the difference between life and death.
My goal for this project was to create a machine learning model that could possibly help reduce response times. In order
to do that, I sought out to create a model that could predict where an incident would occur before it occurred (think
Minority Report but instead 'pre-crime' it's 'pre-EMS incident').

To provide a little more detail, it was my objective to predict 'hot-spots' of where EMS vehicles will be needed based
on the hour of the day and the day of the week.

In addition to this model, I discovered (over the course of my exploratory data analysis) that roughly 1/6 of the
population being tended to by EMS personal refused a trip to the hospital. I set out to understand that refusal and
furthermore to predict when individuals were likely to refuse EMS transport.


## Dataset

The dataset for this project was provided by the City of Austin. The data stretches back five years and provides
incident block location, disposition, and time unit arrived among various other fields. With over 640k
rows and twenty-five features in one EMS dataset alone, I was able to filter the data down significantly without losing
predictive power in my model.

To the City of Austin, specifically ATCEMS, a very big thank you! I hope my analysis helps you in any way, shape, or
form.


## Model Selection

EMS response location data is highly sensitive information. With a specific data (timestamp, Latitude and Longitude) one
can conceivably deduce the identity of the person being tended to. To de-identify the information, The City of Austin
provided census-block location data rather than specific latitude, longitude. Because of the nature of the location
data, I felt the most appropriate model was a KMeans classifier.







## The Model

As stated above, I used a KMeans clustering classifier as my model. For this particular KMeans model, I passed through
the coordinates of past events to try and determine 'hotspots' of where most incidents occur. What the KMeans classifier
does is it finds the center of those 'hotspots' (also known as centroids). The tricky part about KMeans is determining
the optimal number of 'hotspots' to tell the model to create. Using anywhere between seven to ten centroids gave me the
best results. I think of a centroid as an EMS vehicle or an EMS station. The City of Austin has more than ten EMS
vehicles but I wanted to see how much area I could cover with minimal centroids (EMS vehicles).

But I also wanted my model to be adaptable and useful for the City of Austin. As a result, I made the model customizable
and easy to use. The end result is a model that allows the user to input day of week, hour of day, and desired amount of
centroids and it outputs a map showing predicted 'hotspots' based on historical data.



## Patient Refusal Prediction

As stated in my overview above, patients have refused EMS transport in roughly 1/6 of the total incidents in the last
five years.

