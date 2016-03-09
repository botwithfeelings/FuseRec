from __future__ import division
from math import log, sqrt
from pickle import load as pl

import config


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
def get_cosine_similarity_for_user(user, vectors):
    sims = [(key, get_cosine_similarity(vectors[user], data)) for (key, data) in vectors.iteritems() if key != user]
    return sorted(sims, key=lambda x: x[1], reverse=True)


# Get a list of recommendations for a given user ID.
def get_recommendations(user, vectors):
    sims = get_cosine_similarity_for_user(user, vectors)
    print vectors[user]
    print sims[0:config.tuning_param["num_sims"]]

    return


def load_vectors():
    with open(config.rec_data["vectors_weighted"], "rb") as fd:
        vectors = pl(fd)
    return vectors


def main():
    v = load_vectors()
    print v
    # for user in v.iterkeys():
    #     get_recommendations(user, v)
    #     break
    return


if __name__ == "__main__":
    main()
