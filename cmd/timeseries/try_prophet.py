import pandas as pd
import numpy as np
from prophet import Prophet

df = pd.read_csv('~/Downloads/timeseries_data/redis_commands_processed_total/{job="redis_exporter"}.csv')
df['ds'] = pd.to_datetime(df['ds'],unit='s')
df['y'] = df['y'].apply(pd.to_numeric)
# df['y']=np.log(df['y'])
df = df.sort_values(by=['ds'])
print(df.head())

m = Prophet()
m.fit(df)

pd.date_range
future = m.make_future_dataframe(periods=36,freq='2H',include_history=False)

forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

fig1 = m.plot(forecast)
fig1.savefig('forcast.png')

fig2 = m.plot_components(forecast)
fig2.savefig('components.png')


