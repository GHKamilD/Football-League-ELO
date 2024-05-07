import requests
import pandas
from datetime import date, timedelta, datetime
import time
import matplotlib.pyplot as plt



def remove_dates(data, start_date):
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    row_date_from = datetime.strptime(data["From"][0], '%Y-%m-%d').date()
    row_date_to = datetime.strptime(data["To"][0], '%Y-%m-%d').date()
    while row_date_from<start_date and row_date_to<start_date:
        data = data.drop(index=0)
        data.reset_index(drop=True, inplace=True)
        row_date_from = datetime.strptime(data["From"][0], '%Y-%m-%d').date()
        row_date_to = datetime.strptime(data["To"][0], '%Y-%m-%d').date()
        #print(row_date_from)
        #print(row_date_to)
    #start_date = start_date.split("-")
    #start_date = [int(x) for x in start_date]
    #start_date = date(start_date[0], start_date[1], start_date[2])
    #row_date = data["From"][0]
    #print(row_date)
    #print(start_date<date(2024,12,12))
    return data
kraje = ["POL", "GER", "FRA"]
daty = [date(1970,1,1), date(1980,1,1), date(1990,1,1)]
numbs = [5,2,20]
testing = {kraj:{data:[numbs[0], numbs[1]] for data in daty} for kraj in kraje}
print(testing)
def make_average(dict):
    for count in dict.keys():
        for value in dict[count].keys():
            if dict[count][value][1]!=0:
                dict[count][value] = dict[count][value][0]/dict[count][value][1]
    return dict
testing = make_average(testing)
print(testing)

base_url = "http://api.clubelo.com/"

start_date = date(1970, 2, 1)
end_date = date(2024, 3, 31)

# Loop through all the dates in 2023
delta = end_date - start_date
teams = set()
for i in range(0,delta.days + 1,365):
    current_date = start_date + timedelta(days=i)
    url = f"{base_url}{current_date.strftime('%Y-%m-%d')}"
    print(current_date.strftime('%Y-%m-%d'))
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()
    lmao = response.content.decode("utf-8").split("\n")
    test = [item.split(",") for item in lmao[1:]]
    data = pandas.DataFrame(test, columns=lmao[0].split(","))
    teams.update(data["Club"])
    print(end_time-start_time)
    print(url)

print(teams)
teams.remove(None)
    # Send a GET request to the URL
"""response = requests.get("http://api.clubelo.com/2023-12-31")
lmao = response.content.decode("utf-8").split("\n")
test = [item.split(",") for item in lmao[1:]]
print(test)
dane = pandas.DataFrame(test, columns=lmao[0].split(","))
print(dane)
print(set(dane["Country"]))
print(type(dane["From"][1]))"""
#remove_dates(dane, dane["From"][1])
country_list = ["FRA", "GER", "ENG", "ITA", "ESP"]
today = date.today()
print(today)
country_dicts = {country:{date(1970, 1, 1) + timedelta(days=day):[0,0,[]] for day in range((date(today.year, 12, 31)-date(1970,1,1)).days + 1)} for country in country_list}
hej = datetime.strptime("1997-12-12", '%Y-%m-%d').date()
print(hej)
print(type(hej))
#print(country_dicts)
for club in teams:
    print(club)
    response = requests.get(f"{base_url}{club}".replace(" ",""))
    lmao = response.content.decode("utf-8").split("\n")
    test = [item.split(",") for item in lmao[1:]]
    dane = pandas.DataFrame(test, columns=lmao[0].split(","))
    dane = remove_dates(dane, "1970-01-01")
    if datetime.strptime(dane["From"][0], '%Y-%m-%d').date() < date(1970, 1, 1): dane.loc[0, "From"] = "1970-01-01"
    #dane.loc[0, "From"] = "1970-01-01"
    kraj = dane["Country"][0]
    if kraj == "FRG" or kraj == "GDR": kraj = "GER"
    if kraj in country_list:
        for i in range(len(dane["From"])):
            if dane["Country"][i] == "GDR": continue
            if dane["Country"][i] == "FRG":
                dane.loc[i,"Country"] = "GER"
            #print(dane["From"])
            if dane["From"][i]==None: break
            if dane["Level"][i] != '1': continue
            #print(dane["From"][i])
            first_date = datetime.strptime(dane["From"][i], '%Y-%m-%d').date()
            last_date = datetime.strptime(dane["To"][i], '%Y-%m-%d').date()
            delta = last_date - first_date
            x = delta.days
            #print(x)
            for j in range (x+1):
                country_dicts[kraj][first_date+timedelta(days=j)][0] += float(dane["Elo"][i])
                country_dicts[kraj][first_date + timedelta(days=j)][1] += 1
                country_dicts[kraj][first_date + timedelta(days=j)][2].append(club)
                #print(country_dicts[kraj][first_date+timedelta(days=j)])
        #country_dicts[dane["Country"]][]
    #print(dane)
#country_dicts = make_average(country_dicts)
rows = []
for country, dates in country_dicts.items():
    for date, values in dates.items():
        row = {'Country': country, 'Date': date, 'Elo Sum': values[0], 'Number of Teams': values[1], 'Clubs': values[2]}
        rows.append(row)

# Convert the list of dictionaries to a DataFrame
df = pandas.DataFrame(rows)

# Save the DataFrame to a CSV file
df.to_csv('elo_ratings.csv', index=False)
