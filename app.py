# import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app
app = Flask(__name__)


# Define what to do when a user hits the home page route
@app.route("/")
def welcome():
    return (
	f"Available Routes:<br/>"
	f"/api/v1.0/precipitation<br/>"
	f"/api/v1.0/stations<br/>"
	f"/api/v1.0/tobs<br/>"
	f"/api/v1.0/yyyy-mm-dd<br/>"
	f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd")


# Define what to do when a user hits the precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
	
	# create the session
	session = Session(engine)

	# query the precipitation data
	results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").all()

	session.close()

	# convert the list to Dictionary
	precip_results = []
	for date, prcp in results:
		precip_dict = {}
		precip_dict["date"] = date
		precip_dict["prcp"] = prcp
		precip_results.append(precip_dict)

	return jsonify(precip_results)

# Define what to do when a user hits the station route
@app.route("/api/v1.0/stations")
def stations():

	# create the session
	session = Session(engine)

	# query the station data
	active_station = session.query(Station.station).order_by(Station.station).all()

	session.close()
	
	# convert the tuple to a list
	stations = list(np.ravel(active_station))

	return jsonify (stations)

# Define what to do when a user hits the tobs route
@app.route("/api/v1.0/tobs")
def tobs():
	
	# create the session
	session = Session(engine)

	# query the tobs data
	temperature = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == "USC00519281").\
	filter(Measurement.date >= "2016-08-23").\
	filter(Measurement.date <= "2017-08-23").all()

	session.close()

	# convert the tuple to a list
	temp = list(np.ravel(temperature))

	return jsonify(temp)

# Define what to do when a user enters the start date
@app.route("/api/v1.0/<start>")
def Start_date(start):

	# create the session
	session = Session(engine)

	# query the data
	select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
	results = session.query (*select).filter(Measurement.date >= start).all()

	session.close()

	# convert the list to Dictionary
	tobs_start = []
	for min, avg, max in results:
		start_date_tobs = {}
		start_date_tobs["min"] = min
		start_date_tobs["avg"] = avg
		start_date_tobs["max"] = max
		tobs_start.append(start_date_tobs)
	return jsonify(tobs_start)

# Define what to do when a user enters the start date and end date
@app.route("/api/v1.0/<start>/<end>")
def Start_end_date(start, end):

	# create the session
	session = Session(engine)

	# query the data
	select = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
	results_end = session.query (*select).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

	session.close()

	# convert the list to Dictionary
	tobs_start_end = []
	for min, avg, max in results_end:
		start_end_tobs = {}
		start_end_tobs["min"] = min
		start_end_tobs["avg"] = avg
		start_end_tobs["max"] = max
		tobs_start_end.append(start_end_tobs)
	return jsonify(tobs_start_end)

if __name__ == "__main__":
    app.run(debug=True)
