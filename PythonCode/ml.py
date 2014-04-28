from sklearn import svm
from collections import Counter
import json
import numpy as np
from sklearn.cross_validation import train_test_split

colors = ['red', 'blue', 'green', 'purple', 'yellow', 'nothing']

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

ratio = 0.9
train_targets, test_targets, train_features, test_features = train_test_split(targets, features, test_size=0.1, random_state=42)

clf = svm.SVC()

clf.fit(train_features, train_targets)

print "Training Complete"

everything = Counter(test_targets)
correct = Counter()
for feature, target in zip(test_features, test_targets):
	if clf.predict(feature) == target:
		correct.update(str(target))
for key in everything:
    print "%s: %f" % (colors[key], (correct[str(key)]/float(everything[key])))	
print sum(correct.values())/float(sum(everything.values()))	
