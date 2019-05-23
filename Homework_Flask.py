
#dependencies
from flask import Flask, jsonify

import numpy as np
import datetime as dt
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite?check_same_thread=False")

Base = automap_base()

Base.prepare(engine, reflect=True)

#CSV Connections
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our sess ion (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

# Flask Routes (Home Page)
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startandenddates/2017-08-22/2018-08-23"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of one year of precipitation recorded"""
    # Query 1 year of precipitation
    date = dt.date(2017,8,23) - dt.timedelta(days=365)

    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > date).order_by(Measurement.date).all()
    
    rain_list = dict(precip)

    return jsonify(rain_list)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations"""

    station_data = session.query(Station.station,Station.name).all()

    station_list = list(station_data)

    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def temperatures():
    """Return a list of all temperatures for the previous year"""
    date_one = dt.date(2017,8,23) - dt.timedelta(days=365)

    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > date_one).order_by(Measurement.date).all()
    
    temp_list = list(temp)

    return jsonify(temp_list)

@app.route("/api/v1.0/startandenddates/2017-08-22/2018-08-23")
def start_and_end_day(start, end):
    start_and_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    # Convert the List of Tuples Into Normal List
    mins_maxes_averages = list(start_and_end_day)
    # Return JSON List 
    return jsonify(mins_maxes_averages)



if __name__ == '__main__':
    app.run(debug=True)