from __future__ import division
from random import choice

import utility
import config


# Get recommendations from the similarity matrix given the user data.
def get_recommendations(sm, data):
    # Get similarity scores - average of similarity values of functions used by the user,
    # in the similarity matrix for functions not used by the user.
    sim_scores = {f: utility.average([v for (fo, v) in sm[f].iteritems() if fo in data.keys()])
                  for f in sm.iterkeys() if f not in data.keys()}

    # Sort by the scores.
    recs = sorted(sim_scores, key=sim_scores.get, reverse=True)

    if len(recs) > config.tuning_param["num_recs"]:
        recs = recs[0: config.tuning_param["num_recs"]]

    return recs


def do_cv(sm, test):
    # Do cross validation for each entry in the testing set.
    success = 0
    for data in test.itervalues():
        # The function to be removed.
        test_func = choice(data.keys())
        data.pop(test_func)

        # Get the recommendation for the user in training data.
        if test_func in get_recommendations(sm, data):
            success += 1

    return success


def do_item_cf():
    # Need only the testing data and the similarity matrix.
    _, test = utility.load_vectors()
    sm = utility.load_sim_matrix()

    # Get the success rate from the
    success = [do_cv(sm, test) for _ in range(config.cv_runs)]

    # Print the average success rate
    print utility.average(success)

    return


def main():
    do_item_cf()
    return


if __name__ == "__main__":
    main()
