from math import sqrt
from pickle import load

import config


def load_sim_matrix():
    with open(config.rec_data["similarity_matrix"], "rb") as fd:
        sm = load(fd)
    return sm


def load_vectors(weighted):
    vector_file = config.rec_data["vectors"]
    if weighted:
        vector_file = config.rec_data["vectors_weighted"]
    with open(vector_file, "rb") as fd:
        v = load(fd)
    return v


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
    norm_x = sqrt(sum([v**2 for v in x.itervalues()]))
    norm_y = sqrt(sum([v**2 for v in y.itervalues()]))

    try:
        res /= (norm_x * norm_y)
    except ZeroDivisionError:
        # In case we were bad somewhere.
        res = 0

    return res
