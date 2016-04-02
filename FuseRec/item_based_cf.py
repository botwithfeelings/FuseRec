from __future__ import division
from random import choice

import utility
import config
from state import *


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
    outfile_string = "item_slice" + str(config.num_slices) \
     + "_rec" + str(config.tuning_param['num_recs']) + ".txt"
    rates = list()
    st = state('Item Based', rates, outfile_string, "INFO", config.num_slices, config.tuning_param['num_recs'])
    for i in xrange(st.num_slices):
        st.cur_slice += 1 
        train, test = utility.get_data_split(data, i)
        success = do_item_cf(train, test)
        st.rates = (success,len(test))
    return st


def main():
    final_state = do_cv()
    print(final_state)
    final_state.term()
    return


if __name__ == "__main__":
    main()
