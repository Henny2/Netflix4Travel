import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, Response, render_template
import json
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from joblib import dump, load 
import re

#from flask_cors import CORS, cross_origin

#Load CF Model:

'''

Select model path based on OS

'''
# for windows:
#clf = load('../CF-KNNBasic.joblib')
# for mac: 
clf = load('CF-KNNBasic.joblib')
test_username = 'Swimmy128'

#CF Recommendation Setup Functions:
def setup_user_ratings(username, locations):
    
    rating_table = [[username, loc] for loc in locations]
    ratings_df = pd.DataFrame(rating_table)
    ratings_df.columns = ['username', 'location']
    
    return ratings_df
    
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
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/user_selection")
def user_selection_display():

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
    
    print(locations_list)
    
    return render_template("user_selection.html", locations = locations_list)

@app.route("/recommendation")
def show_recommendation():
    #request.args.get extracts the data posted by the <input> tag with name = 'arg'
    input_id = request.args.get('hidden-list')
    input_id = re.sub(r'\n','', input_id) #remove extra characters
    input_id = input_id.split(',') #split locations:

    new_rating = pd.Series([5]*len(input_id), index = input_id, name = 'new')

    locations = db.engine.execute("SELECT location_name FROM locations_table")
    locations_df = pd.DataFrame(locations.fetchall())
    ratings_df = setup_user_ratings(test_username, locations_df.values.flatten())

    updated_df = input_ratings(ratings_df, new_rating)

    recommendation = pd.DataFrame(clf.test(get_model_input(updated_df)))
    recommendation.sort_values(by = ['r_ui', 'est'], ascending = [True, False], inplace = True)
    print(recommendation)

    user_recommendations = recommendation['iid'][0:3]
    print(user_recommendations.iloc[0])

    top_recommendation = user_recommendations.iloc[0]

    return render_template('recommendation.html', recommended_loc = top_recommendation)



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