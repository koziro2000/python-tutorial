# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 12:26:08 2018

@author: jroh
"""

from sklearn import svm
from sklearn import datasets

clf = svm.SVC()
iris = datasets.load_iris()

X, y = iris.data, iris.target

clf.fit(X, y)

list(clf.predict(iris.data[:3]))

clf.fit(iris.data, iris.target_names[iris.target])
list(clf.predict(iris.data[:3]))


