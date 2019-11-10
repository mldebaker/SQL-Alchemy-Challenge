# Import Dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify

# Create Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create Flask
app = Flask(__name__)

# Home route
@app.route("/")


# Precipitation route - http://127.0.0.1:5000/api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    past12mth_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= past12mth_date).all()
# Dict with date as the key and prcp as the value
    precip = {date: prcp for date, prcp in query}
    return jsonify(precip)


# Stations route - http://127.0.0.1:5000/api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    total_stations = session.query(func.count(Station.station)).all()
# Dict with date as the key and prcp as the value
    return jsonify(total_stations)


# Temps route - http://127.0.0.1:5000/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    past12mth_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temps_12_months = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.station=='USC00519281').\
    filter(Measurement.date >= past12mth_date).all()
# Dict with date as the key and prcp as the value
    return jsonify(temps_12_months)


# Start of app
if __name__ == '__main__':
    app.run()

