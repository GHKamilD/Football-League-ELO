import requests
import pandas
from datetime import date, timedelta, datetime
import time

base_url = "http://api.clubelo.com/"

year = 1960

def create_teams(country_list, start_date):
    print("bruh1")
    today = date.today()
    delta = date(today.year, 5, 31) - start_date
    teams = {}
    for i in range(0, delta.days + 1, 365):
        current_date = start_date + timedelta(days=i)
        url = f"{base_url}{current_date.strftime('%Y-%m-%d')}"
        print(current_date.strftime('%Y-%m-%d'))
        start_time = time.time()
        response = requests.get(url)
        end_time = time.time()
        lmao = response.content.decode("utf-8").split("\n")
        test = [item.split(",") for item in lmao[1:]]
        data = pandas.DataFrame(test, columns=lmao[0].split(","))
        mask = data['Country'].isin(country_list)
        # teams.update(data["Club"])
        year_teams = dict(zip(data[mask]['Club'], data[mask]['Country']))
        teams.update(year_teams)
        print(end_time - start_time)
        print(url)
    return teams

def create_ratings(teams, country_list):
    print("bruh3")
    from datetime import date
    def remove_dates(data, start_date):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        row_date_from = datetime.strptime(data["From"][0], '%Y-%m-%d').date()
        row_date_to = datetime.strptime(data["To"][0], '%Y-%m-%d').date()
        while row_date_from < start_date and row_date_to < start_date:
            data = data.drop(index=0)
            data.reset_index(drop=True, inplace=True)
            row_date_from = datetime.strptime(data["From"][0], '%Y-%m-%d').date()
            row_date_to = datetime.strptime(data["To"][0], '%Y-%m-%d').date()
        return data

    def make_average(dict):
        for count in dict.keys():
            for value in dict[count].keys():
                if dict[count][value][1] != 0:
                    dict[count][value] = dict[count][value][0] / dict[count][value][1]
        return dict

    today = date.today()
    country_dicts = {country: {date(year, 1, 1) + timedelta(days=day): [0, 0] for day in range((date(today.year, 12, 31) - date(year, 1, 1)).days + 1)} for country in country_list}
    for club in teams:
        print(club)
        print(club)
        response = requests.get(f"{base_url}{club}".replace(" ", ""))
        lmao = response.content.decode("utf-8").split("\n")
        test = [item.split(",") for item in lmao[1:]]
        dane = pandas.DataFrame(test, columns=lmao[0].split(","))
        dane = remove_dates(dane, f"{year}-01-01")
        if datetime.strptime(dane["From"][0], '%Y-%m-%d').date() < date(year, 1, 1): dane.loc[0, "From"] = f"{year}-01-01"
        kraj = dane["Country"][0]
        if kraj == "FRG" or kraj == "GDR": kraj = "GER"
        if kraj in country_list:
            for i in range(len(dane["From"])):
                if dane["Country"][i] == "GDR": continue
                if dane["Country"][i] == "FRG":
                    dane.loc[i, "Country"] = "GER"
                # print(dane["From"])
                if dane["From"][i] == None: break
                if dane["Level"][i] != '1': continue
                # print(dane["From"][i])
                first_date = datetime.strptime(dane["From"][i], '%Y-%m-%d').date()
                last_date = datetime.strptime(dane["To"][i], '%Y-%m-%d').date()
                delta = last_date - first_date
                x = delta.days
                # print(x)
                for j in range(x + 1):
                    country_dicts[kraj][first_date + timedelta(days=j)][0] += float(dane["Elo"][i])
                    country_dicts[kraj][first_date + timedelta(days=j)][1] += 1
    country_dicts = make_average(country_dicts)

    rows = []
    for country, dates in country_dicts.items():
        for date, values in dates.items():
            row = {'Country': country, 'Date': date, 'Average ELO': values}
            rows.append(row)

    # Convert the list of dictionaries to a DataFrame
    df = pandas.DataFrame(rows)

    df['Date'] = pandas.to_datetime(df['Date'])

    # Save the DataFrame to a CSV file
    df.to_csv('elo_ratings.csv', index=False)
