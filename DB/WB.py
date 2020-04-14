import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, Response, render_template, session
import json
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from joblib import dump, load 
import re
import time
import csv

#from flask_cors import CORS, cross_origin

#Load CF Model:

'''

Select model path based on OS

'''
# for windows:
#clf = load('../CF-KNNBasic.joblib')
#neighbor_df = pd.read_csv('../neighbor_df.csv', index_col = 0)
# for mac: 
clf = load('CF-KNNBasic.joblib')
neighbor_df = pd.read_csv('/Users/huangheqing/Google Drive (hhq@berkeley.edu)/IEOR 290/Netflix4Travel/neighbor_df.csv', index_col = 0)


test_username = 'KissXX'

#CF Recommendation Setup Functions:
def setup_user_ratings(username, locations):
    
    rating_table = [[username, loc] for loc in locations]
    ratings_df = pd.DataFrame(rating_table)
    ratings_df.columns = ['username', 'location']
    
    return ratings_df

def closest_neighbor(df, x):
    
    closest = np.inf
    neighbor = None
    
    for index, row in df.iterrows():
        dist = np.linalg.norm(row.values[1:]-x)
        if  dist < closest:
            closest = dist
            neighbor = row.Name
    
    return neighbor
    
def input_ratings(ratings_df, loc_ratings):
    '''
    loc_ratings: a list of location-rating in a DF
    '''
    joined_df = ratings_df.join(other = loc_ratings, on='location')
    joined_df.fillna(0, inplace = True)
    joined_df.columns = ['username', 'location', 'rating']

    edit_location_name = joined_df['location'].apply(lambda x: re.sub('\r', '', x))
    joined_df['location'] = edit_location_name

    return joined_df
    
def get_model_input(ratings_df): 
    
    username = ratings_df['username']
    
    return ratings_df.apply(lambda x: (x['username'], x['location'], x['rating']), axis = 1)
    
def no_input(x):

    if len(x) == 0:
        return "No Input"
    else: 
        return x

# Log user activities at the recommendation page
def activitylog(timestamp, username, email, phone, selection_1, selection_2, selection_3, neighbor, recommendation):
    with open('Activity_Log.csv', 'a+', newline = '') as log:
        fieldnames = ['timestamp','username','email','phone','selection_1','selection_2','selection_3','neighbor','recommendation']
        writer = csv.DictWriter(log, fieldnames = fieldnames)
        writer.writerow(
            {
            'timestamp': timestamp,
            'username': username,
            'email': email,
            'phone': phone,
            'selection_1': selection_1,
            'selection_2': selection_2,
            'selection_3': selection_3,
            'neighbor': neighbor,
            'recommendation': recommendation
            })
    print(username + "'s information is logged!")

# specify database configurations
config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    #lance
    #'password': 'mypass',
    #heqing
    'password': '0421',
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
app.secret_key = 'datax'
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/user_selection", methods = ['POST', 'GET'])
def user_selection_display():
    
    #get user name
    if request.method == "POST":

        user_info_request = request.form
        
        instance_phone = user_info_request['phone']
        instance_email = user_info_request['email']
        instance_username = user_info_request['name']

        #Use session to pass values between packages/webpages 

        session['session_name'] = user_info_request['name']
        session['session_phone'] = user_info_request['phone']
        session['session_email'] = user_info_request['email']

        print('test_name')


    locations_list = []

    #Pick six random locations to display:

    locations = db.engine.execute("SELECT location_id, location_name FROM locations_table")
    locations_df = pd.DataFrame(locations.fetchall())
    locations_df.columns = ['location_id', 'location_name']

    to_display_index = np.random.choice(locations_df.shape[0]-1, 6, replace = False)

    to_display = locations_df.iloc[to_display_index, 1]
    
    for row in to_display:
        
        #location_name = db.engine.execute("SELECT location_name FROM locations_table WHERE location_id = %s", row[1])
        locations_dict = {}
        locations_dict["location_name"] = row
        locations_list.append(locations_dict)
    
    #print(locations_list)
    #print("in user_selection")
    #print(instance_username)
    
    

    return render_template("user_selection.html", locations = locations_list, instance_user_name = instance_username)

@app.route("/recommendation")
def show_recommendation():
    #request.args.get extracts the data posted by the <input> tag with name = 'arg'
    input_id = request.args.get('hidden-list')
    #print("LOOK HERE!!!!!!")
    #print(type(request))
    input_id = re.sub(r'\n','', input_id) #remove extra characters
    input_id = input_id.split(',') #split locations:
    #print(input_id)

    locations = db.engine.execute("SELECT location_name FROM locations_table")
    locations_df = pd.DataFrame(locations.fetchall())
    #print(locations_df)

    user_input = locations_df.iloc[:, 0].apply(lambda x: 3.5 if x in input_id else 0)
    #print(user_input)
    neighbor = closest_neighbor(neighbor_df, user_input)
    #print(neighbor)

    recs = []
    for item in neighbor_df.columns[1:]:
        recs.append(clf.predict(neighbor, item))

    rec_df = pd.DataFrame(recs).sort_values(by='est', ascending=False)
    recommendation = rec_df.iloc[0, :]['iid']
    
    


    # Get all values in this session
    instance_username = no_input(session.get('session_name', None))
    instance_email = no_input(session.get('session_email', None))
    instance_phone = no_input(session.get('session_phone', None))
    locations_df = session.get('locations_df', None)
    

    # Store values in csv 
    
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    print('=====Values I have so far:=====')
    print(timestamp)
    print(instance_username, instance_phone, instance_email)
    print('=====Input id : three selection of the user =====')
    print(input_id)
    print(input_id[0])
    print('=====User Input : location id, rating=====')
    print(user_input)
    print('=====neighbor=====')
    print(neighbor)
    print('=====recommendation=====')
    print(recommendation)


    activitylog(timestamp = timestamp,
     username = instance_username, 
     email = instance_email, 
     phone = instance_phone, 
     selection_1 = input_id[0], 
     selection_2 = input_id[1], 
     selection_3 = input_id[2], 
     neighbor = neighbor, 
     recommendation = recommendation)

    return render_template('recommendation.html', recommended_loc = recommendation, instance_user_name = instance_username)



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
    
    #print(user_df)

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
    # Store User information
    #global instance_username 
    #global instance_email
    #global instance_phone

    app.run(host="0.0.0.0", debug=True)