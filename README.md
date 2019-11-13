# sqlalchemy-challenge

Basic climate analysis and data exploration of Hawaii climate database using python and sqlalchemy. 

Precipitation analysis:
Designed a query to retrieve the last 12 months of precipitation data.
Loaded the query results into a Pandas DataFrame.
Sorted the DataFrame values by date.
Plotted the results using the DataFrame plot method.

Station Analysis:
Designed a query to calculate the total number of stations.
Designed a query to find the most active stations.
Designed a query to retrieve the last 12 months of temperature observation data (tobs).
Plotted the results as a histogram with bins=12.

Climate app:
Design a Flask API based on the analysis performed with:
homepage (containing list of routes)
precipitation (app that returns JSON representation of date and precipitation dictionary)
station (app that returns JSON list of station)
tobs (app that returns list of date and temperature for the previous year)
start_date (app that returns temp info(min, max, avg) for all the dates with starting date that you input)
start_date/end_date (app that returns temp info(min, max, avg) for all the dates in range of starting-date and end-date that you input)