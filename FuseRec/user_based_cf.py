from __future__ import division

import utility
import config

# The user vectors, weighted and non-weighted.
vectors = dict()
vectors_weighted = dict()


# For a given user u, get back a dictionary of cosine distances of each vector in set v.
def get_cosine_similarity_for_user(user):
    sims = [(key, utility.get_cosine_similarity(vectors_weighted[user], data))
            for (key, data) in vectors_weighted.iteritems() if key != user]
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


def do_user_cf():
    global vectors, vectors_weighted
    vectors, vectors_weighted = utility.load_vectors(False), utility.load_vectors(True)
    recommendations = {user: get_recommendations(user) for user in vectors.iterkeys()}

    # Temporary view.
    print recommendations

    # TODO insert cross validation code here.
    return


def main():
    do_user_cf()
    return


if __name__ == "__main__":
    main()
