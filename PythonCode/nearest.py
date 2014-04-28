from collections import Counter
import json
import numpy as np
from sklearn.cross_validation import train_test_split
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets, linear_model, ensemble, svm
import pylab as pl
import pickle

colors = ['red', 'blue', 'green', 'purple', 'yellow']

attrs = lambda color: [json.loads(line) for line in open('%s.txt' % color, 'r')]

features = []
targets = []
# I know this is gross
for i, color in enumerate(colors):
	color_list = attrs(color)
	targets.extend([i]*len(color_list))
	features.extend(color_list)

targets = np.array(targets)
features = np.array(features)

print "All data loaded!"

n_neighbors = 20

ratio = 0.3
train_targets, test_targets, train_features, test_features = train_test_split(targets, features, test_size=1-ratio)

clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
clf2 = ensemble.RandomForestClassifier(25, criterion="entropy")
clf3 = svm.SVC()

clf.fit(train_features, train_targets)
clf2.fit(train_features, train_targets)
clf3.fit(train_features, train_targets)

pickle.dump(clf, open('knn.pkl', 'w'))
pickle.dump(clf2, open('rfc.pkl', 'w'))
pickle.dump(clf3, open('svm.pkl', 'w'))
print "Training Complete"

print "KNN:"
everything = Counter(test_targets)
correct = Counter()
for feature, target in zip(test_features, test_targets):
	if clf.predict(feature) == target:
		correct.update(str(target))
for key in everything:
    print "%s: %f" % (colors[key], (correct[str(key)]/float(everything[key])))	
print sum(correct.values())/float(sum(everything.values()))

print "RandomForestClassifier: "
everything = Counter(test_targets)
correct = Counter()
for feature, target in zip(test_features, test_targets):
	if clf2.predict(feature) == target:
		correct.update(str(target))
for key in everything:
    print "%s: %f" % (colors[key], (correct[str(key)]/float(everything[key])))	
print sum(correct.values())/float(sum(everything.values()))

print "SVM:"
everything = Counter(test_targets)
correct = Counter()
for feature, target in zip(test_features, test_targets):
	if clf3.predict(feature) == target:
		correct.update(str(target))
for key in everything:
    print "%s: %f" % (colors[key], (correct[str(key)]/float(everything[key])))	
print sum(correct.values())/float(sum(everything.values()))
