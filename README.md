# Netflix4Travel

Contributors:
  1. Melvin Ang
  2. Henrieke Baunack
  3. Heqing Huang
  4. Peijie Li 
  5. Wenxi Li
  6. Lance Zeng

Don't know where to go for summer vacation or spring break? Let us help you out. Netflix4Travel (name TBD) is a personalized, travel itinerary curator. Give us a small taste of what your fun & adventure preferences and a budget, and we'll set you up with the trip of your dreams! 

---
### Enviroment to run website
1. Set up MariaDB in Docker
2. Load data in MariaDB
3. Flask - Python
4. Connect MariaDB in Docker to Flask
5. Execute WB.py in terminal 

#### 1. Set up MariaDB in Docker
- process detailed here: https://github.com/munners17/INFO257-Sp2020/tree/master/docker
- REMEMBER to set your own password

#### 2. Load data in MariaDB
- Connect a front-end to MariaDB; we recommend Datagrip
- process detailed here: https://github.com/munners17/INFO257-Sp2020/blob/master/lectures/01-30/Workshop1.md
- load the data through running Netflix4Travel/DB/Build Netflix4Travel.sql

#### 3. Flask - Python
Special package required:

- from flask import Flask, request, jsonify, Response, render_template, session
- import json
- import mysql.connector
- from flask_sqlalchemy import SQLAlchemy
- from flask_bootstrap import Bootstrap
- from flask_wtf import FlaskForm
- from joblib import dump, load 
- import re

#### 4. Connect MariaDB in Docker to Flask
- We included connection string in Netflix4Travel/DB/WB.py, and you need to replace repository and password with your own

#### 5. Execute WB.py in terminal 

- in termial: python WB.py

----
### Setup to run the restaurant webcrawler
#### Needed packages (might have to be installed before running the code)
- import requests
- import pandas as pd
- import time
- import bs4 as bs 

---
### Setup to run the places in SF webcrwaler

MELVIN

---
### Setup to run the CF scripts
#### Needed packages (might have to be installed before running the code)
- import numpy as np
- import pandas as pd
- import tensorflow as tf
- import timeit
- from sklearn.preprocessing import MinMaxScaler
- from plotly.offline import init_notebook_mode, plot, iplot
- import matplotlib.pyplot as plt
- import plotly.graph_objs as go
- from surprise import Reader
- from surprise import Dataset
- from surprise.model_selection import cross_validate
- from surprise import NormalPredictor
- from surprise import KNNBasic
- from surprise import KNNWithMeans
- from surprise import KNNWithZScore
- from surprise import KNNBaseline
- from surprise import SVD
- from surprise import BaselineOnly
- from surprise import SVDpp
- from surprise import NMF
- from surprise import SlopeOne
- from surprise import CoClustering
- from surprise.accuracy import rmse
- from surprise import accuracy
- from surprise.model_selection import train_test_split
