import requests
import pandas
from datetime import date, timedelta, datetime
import time
import os
import create_files
import matplotlib.pyplot as plt

country_list = ["FRA", "GER", "ENG", "ITA", "ESP", "POR", "NED"]
teams = create_files.create_teams(country_list, date(1960, 6, 1))
if not os.path.exists("elo_ratings.csv"): create_files.create_ratings(teams, country_list)
