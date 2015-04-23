import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols

pd.options.mode.chained_assignment = None

data = pd.read_csv("~/Desktop/metis/project_luther/bom_data_w_rt_ratings_budget.csv")

data['budget'] = data['budget'].convert_objects(convert_numeric=True)
data['rt_critics'] = data['rt_critics'].convert_objects(convert_numeric=True)
data['rt_audience'] = data['rt_audience'].convert_objects(convert_numeric=True)
#data['imdb_rating'] = data['imdb_rating'].convert_objects(convert_numeric=True)

data['agg_rating'] = (data['rt_audience'] + data['rt_critics'])/float(2)

data['gross_to_budget'] = data['domestic_total_gross']/data['budget']

sorted_by_ratio = data.sort(columns='gross_to_budget', ascending=False)

show = sorted_by_ratio[['movie_title', 'gross_to_budget', 'genre', 'director']]

print sorted_by_ratio.head(50)

r = sm.ols(formula="domestic_total_gross ~ rt_critics + rt_audience", data=data)

result = r.fit()
print result.params
print result.summary()