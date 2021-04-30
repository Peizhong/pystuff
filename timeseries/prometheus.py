import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import matplotlib.pylab as plt

df = pd.read_csv('D:/Downloads/timeseries_data/redis_commands_processed_total/addr39.csv')
# 拆分训练和测试
df["ds"] = pd.to_datetime(df["ds"], unit='s')
print(df.head())

m = Prophet()
m.fit(df)

future = m.make_future_dataframe(periods=7)

forecast = m.predict(future)
fig=m.plot(forecast)
a = add_changepoints_to_plot(fig.gca(), m, forecast)
plt.savefig("./pp_forecast.png")

## 预测节日
chinese_holiday = pd.DataFrame({
    'holiday':'chinese holiday',
    'ds': pd.to_datetime(['2021-02-10'])
})

print(forecast.columns)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
m.plot_components(forecast)
plt.savefig("./pp_plot_components.png")

# Prophet 不需要特征工程就可以获得趋势