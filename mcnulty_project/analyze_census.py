import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import seaborn as sns
import pydot
import matplotlib.pyplot as plt
from sklearn.externals.six import StringIO
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.learning_curve import learning_curve
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import precision_recall_fscore_support, roc_auc_score, roc_curve, auc

census_data = pd.read_csv("~/Desktop/metis/mcnulty_project/cenus_data.csv", header=None)
print census_data.head()

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

#split data to train and test
train, test = split_data(census_data)

train_X = train.ix[:, :13]
test_X = test.ix[:, :13]
train_y = train.ix[:, 14]
test_y = test.ix[:, 14]

dt_clf = DecisionTreeClassifier(max_depth=5)
accuracy, result, result_prob = train_clf(dt_clf,
    train_X, train_y, test_X, test_y)

