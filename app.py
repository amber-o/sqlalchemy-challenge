import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()
# reflect the tables
base.prepare(engine)

# Save references to each table
measure = base.classes.measurement
stat = base.classes.station

sess = Session(engine)

app = Flask(__name__)

#routes
@app.route("/")
def welcome():
    return(
        f"Welcome<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/<start>/<end>"

    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    precipitation = sess.query(measure.date, measure.prcp).\
        filter(measure.date >= one_year).all()
    
    sess.close()
    precip = { date: prcp for date, prcp in precipitation}

    return jsonify(precip)



@app.route("/api/v1.0/stations")
def stations():
    results = sess.query(stat.station).all()

    sess.close()

    stats = list(np.ravel(results))

    return jsonify(stats)



@app.route("/api/v1.0/tobs")
def temp_monthly():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = sess.query(measure.tobs).\
        filter(measure.station == 'USC00519281').\
        filter(measure.date >= one_year).all()
    
    sess.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)



@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):

    sel = [func.min(measure.tobs), func.avg(measure.tobs), func.max(measure.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")
        results = sess.query(*sel).\
            filter(measure.date >= start).all()
        
        sess.close()

        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    start = dt.datetime.strptime(start, "%m%d%Y")
    end= dt.datetime.strptime(end, "%m%d%Y")

    results = sess.query(*sel).\
        filter(measure.date >= start).\
        filter(measure.date >= end).all()
    
    sess.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)


if __name__ == "__main__":
    app.run(debug=True)