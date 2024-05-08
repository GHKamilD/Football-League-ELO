import matplotlib.pyplot as plt
import pandas
import matplotlib.dates as mdates

plt.ion()



plt.figure(figsize=(10,6))

#plt.style.use('seaborn-darkgrid')
df = pandas.read_csv('elo_ratings.csv', delimiter=',', parse_dates=['Date'])

plt.xlim(df['Date'].min(), df['Date'].max())

# Loop through each country and plot the data
for country in df['Country'].unique():
    country_data = df[df['Country'] == country]
    plt.plot(country_data['Date'].dt.to_pydatetime(), country_data['Average ELO'], label=country)

# Add title and labels
plt.title('Average ELO Rating Over Time by Country')
plt.xlabel('Date')
plt.ylabel('Average ELO')

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

# Add a legend to the plot
plt.legend(title='Country')

plt.savefig('chart.png', dpi= 500)

# Show the plot
plt.show(block= True)

