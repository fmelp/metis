import csv
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.learning_curve import learning_curve
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from scipy.stats import mode



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
train_X = train.ix[:, :15]
train_y = train.ix[:, 16]
test_X = test.ix[:, :15]
test_y = test.ix[:, 16]


knn_3 = KNeighborsClassifier(n_neighbors=5)
knn_3.fit(train_X, train_y)
result = knn_3.predict(test_X)
print accuracy_score(test_y, result)