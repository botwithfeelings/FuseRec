from __future__ import division

from math import sqrt, ceil
from cPickle import load
from numpy import log
import config


# Simple average function.
def average(l):
    if len(l) == 0:
        return 0
    return sum(l)/len(l)


# Yields n chunks from list l.
def get_chunks(l, n):
    size = int(ceil(len(l)/n))
    ret_list = list()
    for i in xrange(0, len(l), size):
        ret_list.append(l[i:i+size])

    return ret_list


# Returns the most popular list of functions from a set of training data.
def generate_most_popular_list(d):
    pop_list = dict()
    for val in d.itervalues():
        pop_list.update((func, pop_list.get(func, 0) + freq) for func, freq in val.iteritems())

    return sorted(pop_list, key=pop_list.get, reverse=True)


# Get training and testing data set from the given data,
# where testing data contains the pairs in the chunk and
# the rest pairs become training data.
def get_data_split(data, chunk):
    if chunk >= config.num_slices:
        raise ValueError("Invalid slice number: " + str(chunk))

    chunks = get_chunks(data.keys(), config.num_slices)
    # assert len(chunks) == config.num_slices

    train = {k: v for (k, v) in data.iteritems() if k not in chunks[chunk]}
    test = {k: v for (k, v) in data.iteritems() if k in chunks[chunk]}

    return train, test


# Natural log of total users / no. of users using function f in vector set v.
def get_inverse_user_freq(f, v):
    return log(len(v)/sum([f in data.keys() for data in v.itervalues()]))


# Get the function-freq inverse-user-freq weighted values for the passed in data.
def get_weighted_vectors(d):
    for (user, data) in d.iteritems():
        # Iterate through and normalize the each user vector.
        user_sum = sum([v for v in data.itervalues()])
        data.update((k, v/user_sum) for (k, v) in data.iteritems())

        # Now get the weighted vector values using inverse user frequency.
        data.update((k, config.tuning_param["alpha"] * v * get_inverse_user_freq(k, d))
                    for (k, v) in data.iteritems())

        d[user] = data
    return d


# Creates a similarity matrix from the given user data.
def generate_similarity_matrix(uv):
    # First retrieve the weighted vectors for the given data.
    vw = get_weighted_vectors(uv)

    # Get set of all the functions used by the users.
    funcs = set()
    for user_data in vw.itervalues():
        funcs.update(user_data.keys())

    # Define function vectors where each vector contains all weighted values of users for this function.
    fv = {f: {u: d.get(f, 0) for (u, d) in vw.iteritems()} for f in funcs}

    # Define similarity matrix, every key value pair describes the cosine similarity between the functions.
    sm = {f: {fo: get_cosine_similarity(fv[f], fv[fo]) for fo in funcs if f != fo} for f in funcs}

    return sm


def load_vectors():
    with open(config.user_data, "rb") as tr:
        data = load(tr)

    return data


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
