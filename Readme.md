
We were able to predict within an average of ___ cars per hour, the amount of traffic this highway would receive per hour. We were able to achieve this by first stationarizing the model, and then using a SARIMAX model.
A presentation of our results can be found here: https://docs.google.com/presentation/d/1rRSCcDYUPoec5JbITOHacauFt0mKyWxhl402t8pavRk/edit?usp=sharing.


# Traffic Flow of Syndey, Australia
- This project aims to predict traffic patterns on the Eastern Distributor Highway (M1) in Sydney, Australia. The data was provided by the government of New South Wales for the Williams Street Exit toll (https://nswtollroaddata.com). With this information, city planners, trucking companies, and commuters can better plan and predict future traffic levels and plan their commutes accordingly.

## Single Day of Forecasting with AR Model
[https://github.com/trevohearn/TrafficFlowData/blob/master/images/ARForecast_byday.png](ARForecast_byday)
- The AR model predictions over the course of one day

## Seven Day Forecasting with ARIMA Model
[https://github.com/trevohearn/TrafficFlowData/blob/master/images/arima_model_71.png](arima_model_71)

## Autocorrelation of Total Volume of Traffic
[https://github.com/trevohearn/TrafficFlowData/blob/master/images/autocorr_totalvolume.png](autocorr_totalvolumne)

## Partial Autocorrelation of Total Volume of Traffic
[https://github.com/trevohearn/TrafficFlowData/blob/master/images/partial_autocorr_weekdiff.png](partial_autocorr_weekdiff)
- This partial autocorrelation uses a feature that is offset by a week
