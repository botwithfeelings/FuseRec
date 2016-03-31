from __future__ import division
from random import choice

import utility
import config


# Get recommendations from the similarity matrix given the single user's data.
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


def do_item_cf(train, test):
    success = 0

    # Generate the similarity matrix for the given data.
    sm = utility.generate_similarity_matrix(train)

    for data in test.itervalues():
        print(".")
        # The function to be removed.
        test_func = choice(data.keys())
        data.pop(test_func)

        # Get the recommendation for the user in training data.
        if test_func in get_recommendations(sm, data):
            success += 1

    return success


def do_cv():
    # Load the user vectors.
    data = utility.load_vectors()

    rates = list()
    for i in xrange(config.num_slices):
        train, test = utility.get_data_split(data, i)
        success = do_item_cf(train, test)
        rates.append((success))
        print("Run " + str(i) + " success rate " + str(float(success)/float(len(test))))

    return rates


def main():
    do_cv()
    return


if __name__ == "__main__":
    main()
