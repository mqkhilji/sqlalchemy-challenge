# Hawaii Climate Analysis and Data Exploration

Introduction: For my holiday vacation in Honolulu, Hawaii, I embarked on a climate analysis and data exploration project using Python, SQLAlchemy, Pandas, and Matplotlib. This README outlines my process and findings.

# Part 1: Climate Data Analysis
I used the climate_starter.ipynb and hawaii.sqlite files for this analysis.

Here are the Steps:
- Database Connection: Utilized SQLAlchemy's create_engine() to connect to the SQLite database.
- Reflecting Tables into Classes: Employed automap_base() to reflect the tables into classes, namely station and measurement.
- Session Linking: Created a SQLAlchemy session to link Python to the database.

Precipitation Analysis:
- Found the most recent date in the dataset.
- Retrieved the previous 12 months of precipitation data.
- Loaded the data into a Pandas DataFrame and sorted it by date.
- Plotted the data using Matplotlib and calculated summary statistics with Pandas.

Station Analysis:
- Conducted a query to calculate the total number of stations.
- Identified the most active station and calculated its lowest, highest, and average temperatures.
- Retrieved and plotted the last 12 months of temperature observation data (TOBS) for the most active station.


# Part 2: Flask Climate App Design
I designed a Flask API based on my queries.

Routes:
- Home (/): Lists all available routes.
- Precipitation (/api/v1.0/precipitation): Returns a JSON list of precipitation data for the last 12 months.
- Stations (/api/v1.0/stations): Provides a JSON list of stations from the dataset.
- Temperature Observations (/api/v1.0/tobs): Shows a JSON list of temperature observations for the most active station over the past year.
- Temperature Statistics (/api/v1.0/<start> and /api/v1.0/<start>/<end>): Returns JSON lists of temperature statistics for given date ranges.


** I ensured proper linking between the station and measurement tables and utilized Flask's jsonify function for API data rendering. **
