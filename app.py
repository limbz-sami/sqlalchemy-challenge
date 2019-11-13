import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

##############################################################
# Database Setup
##############################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)
"""finding date a year from the last date in the sqlitefile"""
end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
year_ago = dt.date(2017, 8, 23)-dt.timedelta(days=365)
session.close()

print(end_date)
print(year_ago)


##############################################################
# Flask Setup
##############################################################
app = Flask(__name__)

##############################################################
#Flask routes
##############################################################
@app.route("/")
def Homepage():
    """ Listing all API routes in the homepage"""
    return(
        f'Welcome to Hawaii climate API!<br/>'
        f'Available routes :<br/><br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/><br/>'
        
        f'/api/v1.0/<start_date><br/>'
        f'(Input start-date(yyyy-mm-dd) to get temperature info(min, max and avg) for all the dates from the start-date to 2017-08-23) <br/><br/>'

        f'/api/v1.0/<start_date>/<end_date><br/>'
        f'(Input start-date/end-date (yyyy-mm-dd) to get temperature info(min, max and avg) for all your dates)<br/>'
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    """ return precipitation data as json"""
    session = Session(engine)
    prcp_list = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()

    session.close()
    
    prcp_data = []
    for date, prcp in prcp_list:
        prcp_dict = {}
        prcp_dict["date"]= date
        prcp_dict["prcp"]= prcp
        prcp_data.append(prcp_dict)
    
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    station_list = session.query(Measurement.station).group_by(Measurement.station).all()
    session.close()

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_ago).\
         order_by(Measurement.date).all()
    
    return jsonify(tobs_query)

@app.route ("/api/v1.0/<start_date>")
def weather(start_date):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).group_by(Measurement.date).all()
    session.close()
    return(jsonify(results))

        
@app.route ("/api/v1.0/<start_date>/<end_date>")
def weather_info(start_date, end_date):
    session = Session(engine)
    range_results = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.date).all()
    session.close()
    return(jsonify(range_results))

if __name__ == "__main__":
    app.run(debug=True)