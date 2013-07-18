import time
import sofiapy

from sklearn.datasets import make_classification
from sklearn.cross_validation import KFold
from sklearn.grid_search import IterGrid

def _test_data():
    X, y = make_classification(
            n_features=5, n_redundant=1, n_informative=4,
            random_state=1, n_clusters_per_class=1)
    return X, y

if __name__ == '__main__':
    X, y = _test_data()

    param_grid = {
        'lambda' : [0.0001, 0.001, 0.01, 0.1, 0.5, 1],
    }

    cv = 5
    param_errors = {}

    for params in IterGrid(param_grid):
        cv_runs = []
        start = time.clock()

        for train, test in KFold(len(X), cv, indices=False):
            train_X, train_y = X[train], y[train]
            test_X, test_y = X[test], y[test]

            model = sofiapy.PegasosLogisticRegression(lreg=params['lambda'])
            model.fit(train_X, train_y)
            cv_runs.append(model.score(test_X, test_y))

        end = time.clock()

        mean_cv_acc = sum(cv_runs)/len(cv_runs)
        print '\navg test acc %.5f for %s' % (mean_cv_acc, params)
        print '%d-fold CV took %f seconds' % (cv, (end-start))
        param_errors[mean_cv_acc] = params

    best_error = sorted(param_errors.keys(), reverse=True)[0]
    print '\nacc=%.5f for %s' % (best_error, param_errors[best_error])

