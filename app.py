import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# create engine
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def homepage():
    """List all available api routes."""
    return (
        f"Welcome!<br/>"
        f"Where dates are needed, enter date between 2010-01-01 and 2017-08-23.<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/Enter start date<br/>"
        f"/api/v1.0/Enter start date/Enter end date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > year_ago).order_by(Measurement.date).all()
    
    session.close()

    # # Convert list of tuples into normal list
    #rain = list(np.ravel(results))

    # def Convert(a):
    #     it = iter(a)
    #     dic = dict(zip(it,it))
    #     return dic

    # rain_dict = Convert(rain)
    precip=[]
    for date,prcp in results:
        rain_dict={}
        rain_dict["date"]=date
        rain_dict["precipitation"]=prcp
        precip.append(rain_dict)


    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    
    session = Session(engine)

    results = session.query(Station.name).all()

    session.close()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date > year_ago).all()
    
    session.close()

    precip=[]
    for date,prcp in results:
        rain_dict={}
        rain_dict["date"]=date
        rain_dict["precipitation"]=prcp
        precip.append(rain_dict)

    return jsonify(precip)

@app.route("/api/v1.0/<start>")
def temps(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()

    results = list(np.ravel(results))
    
    keys = ['Minimum Temp','Maximum Temp', 'Average Temp']
    temp_dict = dict(zip(keys,results))


    return jsonify(temp_dict)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    #Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date >= start,Measurement.date <= end).all()
    
    session.close()

    results = list(np.ravel(results))
    #temp = [min_temp,max_temp,avg_temp]
    keys = ['Minimum Temp','Maximum Temp', 'Average Temp']
    temp_dict = dict(zip(keys,results))

    return jsonify(temp_dict)

if __name__ == '__main__':
    app.run(debug=True)
