from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import csv
import pandas as pd
import numpy as np
import seaborn as sns
import pydot
import matplotlib.pyplot as plt
from sklearn.externals.six import StringIO
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.learning_curve import learning_curve
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score, roc_curve, auc

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
new['party'] = data['party'].apply(lambda x: 1 if x == 'republican' else 0)

def split_data(data):
    """
    @param -> data : pandas DataFrame
    @return -> train, test : split into 2 pandas DFs with NO HEADERS
    """
    train, test = train_test_split(data)
    train = pd.DataFrame(train)
    test = pd.DataFrame(test)
    return train, test


def train_clf(clf, train_X, train_y, test_X, test_y):
    '''
    @param -> clf : classifier you want to use, must be set up before
              train_X,train_y,test_X,test_y : data split into train and test
                                               and X and y
    @return -> accuracy : accuracy of model (correct pred / len(test_y))
               result : np array of binary classification results
               result_prob : np array of classification results with probabilities

    '''
    clf.fit(train_X, train_y)
    result_prob = clf.predict_proba(test_X)
    result = clf.predict(test_X)
    accuracy = accuracy_score(test_y, result)
    return accuracy, result, result_prob


def plot_roc(test_y, result_prob):
    '''
    @param -> test_y : the original y (actual values for the pred)
              result_prob : classification results with probabilities
    @return -> NULL : only displays a graph
    '''
    false_positive_rate, recall, thresholds = roc_curve(test_y, result_prob[:,1])
    roc_auc = auc(false_positive_rate, recall)
    plt.title('Receiver Operating Characteristic')
    plt.plot(false_positive_rate, recall, 'b', label='AUC = %0.2f' % roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.ylabel('Recall')
    plt.xlabel('Fall-out')
    plt.show()

#split data into train and test and X and y
train, test = split_data(new)
train_X = train.ix[:, :15]
train_y = train.ix[:, 16]
test_X = test.ix[:, :15]
test_y = test.ix[:, 16]


#make a deicision tree classifier with max_depth = 3
dec_tree_clf = DecisionTreeClassifier(max_depth=3)
dec_tree_accuracy, dec_tree_result, dec_tree_result_prob = train_clf(dec_tree_clf, train_X, train_y, test_X, test_y)

#create pdf of tree
dot_data = StringIO()
export_graphviz(dec_tree_clf, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("tree.pdf")


#challenge 1:
#   look at this plot and tree.pdf
plot_roc(test_y, dec_tree_result_prob)
print "Decision Tree Accuracy (depth=3): " + str(dec_tree_accuracy)


#challenge 2
#   use similar tools

#read and prep movie data
data = pd.read_csv("~/Desktop/metis/challenge_4/2013_movies.csv")
data = data.dropna(subset=['Rating'])
data = data[['Budget','DomesticTotalGross', 'Runtime', 'Rating']]
data = data.convert_objects(convert_numeric=True)
data = data.dropna()

tr_mov, ts_mov = split_data(data)
tr_mov_X = tr_mov.iloc[:,0:2]
ts_mov_X = ts_mov.iloc[:,0:2]
tr_mov_y = tr_mov.loc[:, 3]
ts_mov_y = ts_mov.loc[:, 3]


#decision tree classifier
mov_dec_tree_clf = DecisionTreeClassifier(max_depth=4)
mov_dec_tree_accuracy, mov_dec_tree_result, mov_dec_tree_result_prob = train_clf(mov_dec_tree_clf,
    tr_mov_X, tr_mov_y, ts_mov_X, ts_mov_y)

#pdf of tree
#look at tree2.pdf
dot_data = StringIO()
export_graphviz(mov_dec_tree_clf, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("tree2.pdf")

#challenge 2:
#   look at this plot and tree2.pdf
plot_roc(test_y, dec_tree_result_prob)
print "Decision Tree Accuracy (depth=4): " + str(mov_dec_tree_accuracy)

##challenge 3
#   titanic data
tit = pd.read_csv("~/Desktop/metis/challenge_4/train.csv")
print tit.head()
tit = tit[['Survived', 'Pclass', 'Sex', 'Age',
            'SibSp', 'Parch', 'Fare']]
#make male/female binary, where 1 == male, 0 == female
tit['Sex'] = tit['Sex'].apply(lambda x: 1 if x == 'male' else 0)
tit = tit.convert_objects(convert_numeric=True)
tit.dropna(inplace=True)

tit_train, tit_test = split_data(tit)


tit_test_y = tit_test.loc[:, 0]
tit_train_y = tit_train.loc[:, 0]
#keep only columns that are useful for analysis
tit_test_X = tit_test.ix[:, 1:]
tit_train_X = tit_train.ix[:, 1:]

tit_train_X = tit_train_X.convert_objects(convert_numeric=True)
tit_test_X = tit_test_X.convert_objects(convert_numeric=True)
print tit_train_X.dtypes

#decision tree classifier for titanic data
tit_dt_clf = DecisionTreeClassifier(max_depth=5)
tit_accuracy, tit_result, tit_result_prob = train_clf(tit_dt_clf,
    tit_train_X, tit_train_y, tit_test_X, tit_test_y)

#pdf of tree
#look at tree2.pdf
dot_data = StringIO()
export_graphviz(tit_dt_clf, out_file=dot_data)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("tree_tit.pdf")

plot_roc(tit_test_y, tit_result_prob)
print "Decision Tree Accuracy (depth=5): " + str(tit_accuracy)

