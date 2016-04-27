from __future__ import division
import numpy as np

import utility
import config
from state import *


# For a given user u, get back a list of tuples (user_id, cosine distances from given user).
def get_cosine_similarity_for_user(vw, user):
    sims = [(key, utility.get_cosine_similarity(vw[user], data))
            for (key, data) in vw.iteritems() if key != user]
    return sorted(sims, key=lambda x: x[1], reverse=True)


# Get a list of recommendations for a given user ID.
def get_recommendations(data, user, cache):
    # Get the weighted vector for current data.
    vw = utility.get_weighted_vectors(data, cache)

    # Get the sorted similarity values for the given user.
    sims = get_cosine_similarity_for_user(vw, user)

    sims_exp_freq = dict()

    # Only look into the number of similars permitted.
    for sim in sims[0:config.tuning_param["num_sims"]]:
        # Add recommendations with expected frequency, basically the cumulative relative frequency of the similars.
        # Recommendations are those functions that are in the similars but not in the input user vector functions.
        sim_user = sim[0]
        sim_values = data[sim_user]
        c_sum = sum(v for v in sim_values.itervalues())
        sims_exp_freq.update((k, sims_exp_freq.get(k, 0) + config.tuning_param["expected_freq_weight"] * (v/c_sum))
                             for (k, v) in sim_values.iteritems() if k not in data[user].keys())

    # Sort based on the expected frequency.
    recs = sorted(sims_exp_freq, key=sims_exp_freq.get, reverse=True)

    # Limit to number of recommendations in config.
    if len(recs) > config.tuning_param["num_recs"]:
        recs = recs[0: config.tuning_param["num_recs"]]

    return recs


def generate_usage_cache(data):
    cache = dict()
    for d in data.itervalues():
        cache.update((func, cache.get(func, 0) + 1) for (func, freq) in d.iteritems())
    return cache


def add_to_cache(cache, data):
    cache.update((func, cache.get(func, 0) + 1) for (func, freq) in data.iteritems())
    return cache


def remove_from_cache(cache, data):
    cache.update((func, cache.get(func, 0) - 1) for (func, freq) in data.iteritems())
    return cache


def do_user_cf(train, test):
    # Cache that contains how many user uses a certain function.
    usage_cache = generate_usage_cache(train)
    success = 0

    for (user, data) in test.iteritems():
        # The function to be removed at random.
        test_func = np.random.choice(data.keys())
        data.pop(test_func)

        # Update the cache with the test case.
        usage_cache = add_to_cache(usage_cache, data)

        # Add this modified vector to the training set.
        train[user] = data

        # Get the recommendation for the user in training data.
        if test_func in get_recommendations(train, user, usage_cache):
            success += 1

        # Removed the test user from the training data for next iteration.
        train.pop(user)

        # Update the cache again.
        usage_cache = remove_from_cache(usage_cache, data)

    return success


def do_cv():
    # Load the user vectors.
    data = utility.load_vectors()
    outfile_string = "user_slice" + str(config.num_slices) + "_rec" \
        + str(config.tuning_param['num_recs']) + "_users" + str(config.tuning_param['num_sims']) + ".txt"
    rates = list()
    st = state('User Based', rates, outfile_string, "INFO",
               config.num_slices, config.tuning_param['num_recs'], config.tuning_param['num_sims'])
    # Storage for the success rate.
    for i in range(st.num_slices):
        print "current slice: ", st.cur_slice
        st.cur_slice += 1
        train, test = utility.get_data_split(data, i)
        success = do_user_cf(train, test)
        st.rates = (success, len(test))
    return st


def main():
    final_state = do_cv()
    print final_state
    final_state.term()
    return


if __name__ == "__main__":
    main()
