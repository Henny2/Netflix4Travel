import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, Response, render_template
import json
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
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
    return render_template("user_selection.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)