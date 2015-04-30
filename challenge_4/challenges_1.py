import csv
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.learning_curve import learning_curve

pd.options.mode.chained_assignment = None

headers = ['party', 'handicapped_infants', 'water_project_cost_sharing',
    'adoption_of_the_budget_resolution', 'physician_fee_freeze', 'el_salvador_aid',
    'religious_groups_in_schools', 'anti_satellite_test_ban', 'aid_to_nicaraguan_contras',
    'mx_missile', 'immigration', 'synfuels_corporation_cutback','education_spending',
    'superfund_right_to_sue', 'crime', 'duty_free_exports', 'export_administration_act_south_africa']

# read in data -- NOTE: has no headers
data = pd.read_csv("~/Desktop/metis/challenge_4/house-votes-84.csv", header=None,
    names=headers)

#change yes to 1, no to 0, ? to nan
data[data=='y'] = float(1)
data[data=='n'] = float(0)
data[data=='?'] = np.nan
#fill in nan with avg of column, then round to 0 or 1
new = data.ix[:, 'handicapped_infants':].apply(lambda x: x.fillna(x.mean()), axis=0)
new[new < .5] = float(0)
new[new >= .5] = float(1)
new['party'] = data['party']


def split_data(data):
    """
    @param -> data : pandas DataFrame
    @return -> train, test : split into 2 pandas DFs with NO HEADERS
    """
    train, test = train_test_split(data)
    train = pd.DataFrame(train)
    test = pd.DataFrame(test)
    return train, test

train, test = split_data(new)

#KNN

test_X = test.ix[:, :15]
test_y = test.ix[:, 16]


# knn_3 = KNeighborsClassifier(n_neighbors=5)
# knn_3.fit(train_X, train_y)
# result = knn_3.predict(test_X)
# print accuracy_score(test_y, result)

def find_best_k(train_X, train_y, test_X, test_y):
    best_k_num = 0
    best_k_result = 0
    for i in xrange(1,21):
        knn = KNeighborsClassifier(n_neighbors=i)
        knn.fit(train_X, train_y)
        result = knn.predict(test_X)
        accuracy = accuracy_score(test_y, result)
        if accuracy > best_k_result:
            best_k_result = accuracy
            best_k_num = i
    return 'k = ' + str(i) + ', ' + str(best_k_result)


# LOGISTIC REGRESSION
logit = LogisticRegression()
logit.fit(train_X, train_y)
result = logit.predict(test_X)
print accuracy_score(test_y, result)

# flatui = ["#3498db", "#e74c3c"]
# sns.barplot(x=new['party'],dropna=True, palette=flatui)
# sns.despine(left = True, right = True, bottom = True)
# plt.title('Party Membership')
# plt.xlabel('Party')
# plt.ylabel('Count')
# #plt.xticks(rotation = 60)
# plt.gcf().subplots_adjust(bottom=0.25)
# plt.show()

# data = pd.read_csv("~/Desktop/metis/project_luther/final_data_genre.csv")
# data = data.dropna(subset=['genre'])

# #remove commas from theater number and rank in history
# data['number_theaters'] = data['number_theaters'].apply(lambda x: x.lstrip(',') if type(x) == str else x)
# data['rank_history'] = data['rank_history'].apply(lambda x: str(x).lstrip(','))
# #data['runtime'] = data['runtime'].apply(str)

# # make dummy variables
# # data = pd.concat([data, pd.get_dummies(data, columns=['actors', 'director', 'distributor'])], axis=1)

# data['runtime'] = data['runtime'].apply(lambda a: int(a.split()[0])*60 + int(a.split()[2]))


# # split into train and test
# tr_mov, ts_mov = split_data(data)

# # print data.head(50)


# # readd headers
# headers = ['movie_title', 'domestic_total_gross', 'runtime', 'budget',
# 'release_date', 'distributor', 'genre', 'actors', 'director',
# 'producers', 'rank_year', 'rank_history', 'number_theaters',
# 'close_date', 'imdb_rating', 'metascore_rating', 'rt_critics',
# 'rt_audience', 'video_sales']
# d = dict(zip(range(0,20), headers))
# tr_mov.rename(columns=d, inplace=True)
# ts_mov.rename(columns=d, inplace=True)

# #ts_mov = pd.concat([ts_mov, pd.get_dummies(tr_mov, columns=['actors', 'director', 'distributor'])], axis=1)

# #split into X (all but genre) and y (only genre)
# tr_mov_y = tr_mov['genre']
# #print tr_mov_y.head()
# tr_mov_X = tr_mov.drop(['genre', 'release_date', 'close_date',
#                         'producers', 'rank_history', 'movie_title',
#                         'director', 'distributor', 'actors', 'rank_year'], axis=1)
# print tr_mov_X.head(10)
# ts_mov_y = ts_mov['genre']
# ts_mov_X = ts_mov.drop(['genre', 'release_date', 'close_date',
#                         'producers', 'rank_history', 'movie_title',
#                         'director', 'distributor', 'actors', 'rank_year'], axis=1)

# # predict genres using Logit
# logit = LogisticRegression()
# logit.fit(tr_mov_X, ts_mov_y)
# result = logit.predict(ts_mov_X)
# logit_accuracy = accuracy_score(ts_mov_y, result)
# print logit_accuracy
