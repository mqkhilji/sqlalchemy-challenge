# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt
import os
import numpy as np



#################################################
# Database Setup
#################################################

database_path = os.path.join(os.path.dirname(__file__), "../Resources/hawaii.sqlite")
engine = create_engine(f"sqlite:///{database_path}")


# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Find the most recent date in the data set.
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')

    # Calculate the date one year from the last date in the data set.
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_data = {date: prcp for date, prcp in results}

    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    # Query all stations
    results = session.query(Station.station).all()
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(results))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Determine the most active station ID
    most_active_station_id = session.query(Measurement.station).\
                             group_by(Measurement.station).\
                             order_by(func.count(Measurement.station).desc()).\
                             first()[0]

    # Find the most recent date and calculate one year ago
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Query the last 12 months of TOBS data for the most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= one_year_ago).all()
    session.close()

    # Convert to list of dictionaries
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in results]
    return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start=None):
    # Start a new session
    session = Session(engine)

    try:
        # Convert start to a date object
        start_date = dt.datetime.strptime(start, '%Y-%m-%d')

        # Design a query to retrieve the min, max, and avg temperatures for all dates greater than or equal to the start date
        stats = session.query(func.min(Measurement.tobs), 
                              func.max(Measurement.tobs),
                              func.avg(Measurement.tobs)).\
                filter(Measurement.date >= start_date).all()

        # Close the session
        session.close()

        # Create a dictionary for the results
        temp_stats = [{"TMIN": stat[0], "TMAX": stat[1], "TAVG": stat[2]} for stat in stats]

        return jsonify(temp_stats)

    except ValueError:
        # Close the session in case of an error
        session.close()
        return jsonify({"error": "Invalid date format. Please use YYYY-MM-DD format."}), 400





@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end=None):
    session = Session(engine)

    if end:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    session.close()
    
    # Create a dictionary from the row data and append to a list
    temp_list = [{"TMIN": result[0], "TAVG": result[1], "TMAX": result[2]} for result in results]
    return jsonify(temp_list)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
