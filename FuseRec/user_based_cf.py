from __future__ import division
from math import sqrt
from pickle import load as pl

import config

# The user vectors, weighted and non-weighted.
vectors = dict()
vectors_weighted = dict()


# Get cosine similarity between two vectors x and y.
def get_cosine_similarity(x, y):
    # Swap positions so that we have to do less calculations.
    if len(y) < len(x):
        x, y = y, x

    res = 0
    for key, x_val in x.iteritems():
        res += x_val * y.get(key, 0)
    if res == 0:
        return 0

    # Get normalized vector values.
    norm_x = sum([v**2 for v in x.itervalues()])
    norm_y = sum([v**2 for v in y.itervalues()])

    try:
        res /= sqrt(norm_x * norm_y)
    except ZeroDivisionError:
        # In case we were bad somewhere.
        res = 0

    return res


# For a given user u, get back a dictionary of cosine distances of each vector in set v.
def get_cosine_similarity_for_user(user):
    sims = [(key, get_cosine_similarity(vectors_weighted[user], data)) for (key, data) in vectors_weighted.iteritems()
            if key != user]
    return sorted(sims, key=lambda x: x[1], reverse=True)


# Get a list of recommendations for a given user ID.
def get_recommendations(user):
    sims = get_cosine_similarity_for_user(user)

    recs = dict()
    for t in sims[0:config.tuning_param["num_sims"]]:
        # Add recommendations with expected frequency, basically the cumulative relative frequency of the similars.
        # Recommendations are those functions that are in the similars but not in the input user vector functions.
        sim_values = vectors[t[0]]
        c_sum = sum(v for v in sim_values.itervalues())
        recs.update((k, recs.get(k, 0) + config.tuning_param["expected_freq_weight"] * (v/c_sum))
                    for (k, v) in sim_values.iteritems() if k not in vectors[user].keys())

    return sorted(recs, key=recs.get, reverse=True)


def load_vectors(weighted):
    vector_file = config.rec_data["vectors"]
    if weighted:
        vector_file = config.rec_data["vectors_weighted"]
    with open(vector_file, "rb") as fd:
        v = pl(fd)
    return v


def do_user_cf():
    global vectors, vectors_weighted
    vectors, vectors_weighted = load_vectors(False), load_vectors(True)
    recommendations = dict()
    recommendations.update((user, get_recommendations(user)) for user in vectors.iterkeys())

    # Temporary view.
    print recommendations

    # TODO insert cross validation code here.
    return


def main():
    do_user_cf()
    return


if __name__ == "__main__":
    main()
