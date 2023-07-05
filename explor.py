import pandas as pd
import matplotlib.pyplot as plt
 #load the data
df = pd.read_csv('movies.csv')

df['Release Year'] = pd.to_datetime(df['Release Year'], format='%Y')
df.sort_values(by='Release Year', inplace=True)

plt.plot(df['Release Year'],df['Rating'])
plt.title('Rating vs Release Year')
plt.xlabel('Year')
plt.ylabel('Rating')
plt.show()

plt.scatter(df['Budget'], df['Box Office Earnings'])
plt.title('Budget vs Box Office Earnings')
plt.xlabel('Budget')
plt.ylabel('Box Office Earnings')
plt.show()

correlation_matrix = df[['Rating', 'Budget', 'Box Office Earnings']].corr()

print(correlation_matrix)

import seaborn as sns

sns.heatmap(correlation_matrix, annot=True)
plt.show()