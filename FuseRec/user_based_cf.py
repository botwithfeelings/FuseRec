from __future__ import division
from math import log
from pickle import load as pl

import config


# Natural log of total users / no. of users using function f in vector set v.
def get_inverse_user_freq(f, v):
    return log(len(v)/sum([f in data.keys() for data in v.itervalues()]))


def get_weighted_vectors(vectors):
    for (user, data) in vectors.iteritems():
        # Iterate through and normalize the each user vector.
        user_sum = sum([v for v in data.itervalues()])
        data.update((k, v/user_sum) for (k, v) in data.iteritems())

        # Now get the weighted vector values using inverse user frequency.
        data.update((k, config.tuning_param["alpha"] * v * get_inverse_user_freq(k, vectors))
                    for (k, v) in data.iteritems())

        vectors[user] = data
    return vectors


def load_user_vectors():
    with open(config.rec_data["vectors"], "rb") as fd:
        vectors = pl(fd)
    return vectors


def main():
    v = load_user_vectors()
    v = get_weighted_vectors(v)
    print v
    return


if __name__ == "__main__":
    main()
