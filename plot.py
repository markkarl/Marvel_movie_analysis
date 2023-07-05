import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
#load the data
df = pd.read_csv('movies.csv')
x = df[['Budget', 'Box Office Earnings']]
y = df['Rating']

x = sm.add_constant(x)

model = sm.OLS(y,x)
result = model.fit()

print(result.summary())