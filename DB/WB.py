import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, Response, render_template
import json
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
#from flask_cors import CORS, cross_origin


# specify database configurations
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'mypass',
    'database': 'Netflix4Travel'
}

db_user = config.get('user')
db_pwd = config.get('password')


db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

# specify connection string
connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
print(connection_str)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_str
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/user-profile", methods = ['POST', 'GET'])
def display_user_profile():
    ratings_list = []
    if request.method == 'GET':
        input_id = request.args.get('search')

        result = db.engine.execute("SELECT location_id, rating FROM ratings_table WHERE user_id = %s", input_id)

        #Extract user_name for user
        user_name = db.engine.execute('SELECT username FROM users_table WHERE user_id = %s', input_id)

        #Extract location_name for locations that user has been to:
        locations = db.engine.execute("SELECT location_name FROM locations_table WHERE location_id IN (SELECT location_id FROM ratings_table WHERE user_id = %s)", input_id)

        locations_df = pd.DataFrame(locations.fetchall())
        result_df = pd.DataFrame(result.fetchall())

        combined_df = pd.concat([locations_df, result_df], axis = 1)
        combined_df.columns = ['location_name', 'location_id', 'rating']

    for index, row in combined_df.iterrows():
        #location_name = db.engine.execute("SELECT location_name FROM locations_table WHERE location_id = %s", row[1])
        ratings = {}
        ratings["Destination"] = row['location_name']
        ratings['Rating'] = row['rating']
        ratings_list.append(ratings)

    return render_template(
        #destination is a tag in the html file, we pass in the SQL dictionary dstinations_list
        'user_profile.html', destination = ratings_list)

@app.route('/users', methods = ['POST'])
def display_all_users():
    user_list = []

    users = db.engine.execute("SELECT user_id, username FROM users_table")
    user_df = pd.DataFrame(users.fetchall())
    
    print(user_df)

    for index, row in user_df.iterrows():
        #location_name = db.engine.execute("SELECT location_name FROM locations_table WHERE location_id = %s", row[1])
        user_dict = {}
        user_dict["user_id"] = row[0]
        user_dict['username'] = row[1]
        user_list.append(user_dict)

    return render_template(
        #users is a tag in the html file, we pass in the SQL dictionary dstinations_list
        'users.html', users = user_list)



@app.route('/locations', methods = ['POST'])
def display_all_locations():
    locations_list = []

    locations = db.engine.execute("SELECT location_id, location_name FROM locations_table")
    locations_df = pd.DataFrame(locations.fetchall())

    for index, row in locations_df.iterrows():
        #location_name = db.engine.execute("SELECT location_name FROM locations_table WHERE location_id = %s", row[1])
        locations_dict = {}
        locations_dict["location_id"] = row[0]
        locations_dict['location_name'] = row[1]
        locations_list.append(locations_dict)

    return render_template(
        #locations is a tag in the html file, we pass in the SQL dictionary dstinations_list
        'locations.html', locations = locations_list)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)