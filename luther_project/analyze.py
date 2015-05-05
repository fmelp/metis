import pandas as pd
import numpy as np
import random as rnd
import seaborn as sns
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as sm
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols

pd.options.mode.chained_assignment = None

data = pd.read_csv("~/Desktop/metis/project_luther/final_data_genre.csv")

""" HEADERS:
['movie_title', 'domestic_total_gross', 'runtime', 'budget',
'release_date', 'distributor', 'genre', 'actors', 'director',
'producers', 'rank_year', 'rank_history', 'number_theaters',
'close_date', 'imdb_rating', 'metascore_rating', 'rt_critics',
'rt_audience', 'video_sales']
"""



def make_sets(data_df, test_portion):
    """
    @param -> data_df : a dataframe
           -> test_portion : a float < 1, where test_portion*100 = '%'ge to put in test
    @return -> train_df : portion of data_df allocated to training
               test_df  : portion of data_df allocated to testing
    """

    tot_ix = range(len(data_df))
    test_ix = sorted(rnd.sample(tot_ix, int(test_portion * len(data_df))))
    train_ix = list(set(tot_ix) ^ set(test_ix))

    test_df = data_df.ix[test_ix]
    train_df = data_df.ix[train_ix]

    return train_df, test_df

#get rid of duplicates
data.drop_duplicates(inplace=True)

#fix some of the data
data.budget[889] = 6000000
data.genre[667] = 'Romance'


#keep only comedies that scored 80 or higher in rotten tomatoes critic ratings
data = data[~((data['genre'] == 'Comedy') & (data['rt_critics'] < 80))]
data = data[~((data['genre'] == 'Music') | (data['genre'] == 'Musical') | (data['genre'] == "Documentary"))]
#data = data[~((data['budget'] < 10000000))]




#convert from string to numeric
data['budget'] = data['budget'].convert_objects(convert_numeric=True)
data['rt_critics'] = data['rt_critics'].convert_objects(convert_numeric=True)
data['rt_audience'] = data['rt_audience'].convert_objects(convert_numeric=True)
data['rank_year'] = data['rank_year'].convert_objects(convert_numeric=True)
data['video_sales'] = data['video_sales'].convert_objects(convert_numeric=True)

#create a gross box office / budget ratio column
data['gross_to_budget'] = data['domestic_total_gross']/data['budget']



sorted_by_ratio = data.sort(columns='gross_to_budget', ascending=False)
show = sorted_by_ratio[['movie_title', 'genre', 'rt_critics', 'gross_to_budget']]
print show.head(50)

data1, data2 = make_sets(data, 0.5)

print len(data)

# data = data.dropna(subset=['domestic_total_gross', 'budget'])

# data = data[~((data['budget'] < 300000) | (data['domestic_total_gross'] < 1000000))]
# sorted_by_ratio = data.sort(columns='budget', ascending=True)

#data = data[(data['genre'] == 'Horror') | (data['genre'] == 'Comedy') | (data['genre'] == "Family") | (data['genre'] == 'Drama') | (data['genre'] == "Animation")]





#color = data.Group.map({dut_groups[0]: "r", dut_groups[1]: "b"})
sns.lmplot("budget", "domestic_total_gross", hue="genre", data=data, fit_reg=False, )
sns.plt.ylim(0,500000000)
sns.plt.xlim(0,500000000)
sns.plt.xlabel("Budget")
sns.plt.ylabel("Box Office Gross Revenue")
#g.set(ylim=(0,None))
plt.show()

genres = ['Adventure', 'Animation', 'Comedy', 'Crime', 'Drama',
'Family', 'Fantasy', 'Foreign', 'Historical', 'Horror', 'IMAX', 'Period',
'Romance', 'Sci-Fi', 'Sports', 'Thriller', 'War', 'Western']

beta1 = ['0.160645', '-0.100088', '0.024930', '-0.108570',
'0.005269', '-0.029024', '0.056421', '0.129511', '0.325071', '-0.145994',
'0.745868', '0.089886', '0.129896', '0.065724', '-0.133220', '-0.065099',
'0.090299', '-0.011683']

beta2 = ['0.2220', '0.2518', '0.4824', '0.1300', '0.0595',
'0.4066', '0.0360', '-0.0270', '-0.3744', '0.7052', '-0.9764', '-0.1886',
'0.1004', '-0.0487', '0.0743', '-0.0244', '-0.3144', '0.0708']

beta3 = ['-0.0980','0.3487','0.4078', '-0.3605','-0.1441',
'0.4444','-0.4315','-0.2803','-0.3780','0.6761',
'-0.0000000000000000000001442','-0.2542','0.0949',
'0.0012','0.1963','-0.05','-0.5368', '-0.0459']

beta1 = np.array([float(x) for x in beta1])
beta2 = np.array([float(x) for x in beta2])
beta3 = np.array([float(x) for x in beta3])

genres = np.array(genres)



# r = sm.ols("np.log(domestic_total_gross) ~ C(genre) + number_theaters + rt_critics", data=data)
# result = r.fit()
# print result.params
# print result.summary()
# colors = ['#5B9632', '#27556C']
# sns.set(palette = sns.color_palette(colors, desat = .85), style = 'white')
# sns.barplot(x=data['genre'], y=data['domestic_total_gross'], dropna=True)#, x_order = x)
# sns.despine(left = True, right = True, bottom = True)
# plt.title('Beta Coefficients')
# plt.xlabel('Genres')
# plt.ylabel('Gross Domestic Revenue')
# plt.xticks(rotation = 90)
# plt.gcf().subplots_adjust(bottom=0.25)
# plt.show()

sns.barplot(x=genres, y=beta1, dropna=True, palette="Blues_d")#, x_order = x)
sns.despine(left = True, right = True, bottom = True)
plt.title('Beta Coefficients')
plt.xlabel('Genres')
plt.ylabel('Gross Domestic Revenue')
plt.xticks(rotation = 90)
plt.gcf().subplots_adjust(bottom=0.25)
plt.show()


# pred = result.predict(test, transform=False)
# vals = test['gross_to_budget']

# plt.scatter(pred, vals)
# plt.show()

# plt.hist(result.resid, bins=20)
# plt.ylabel('Box Office Gross to Bugdet Ratio (log-scale)')
# plt.xlabel('Residuals')
# plt.show()

# plt.scatter(data['gross_to_budget'], data['rt_critics'])
# plt.show()
