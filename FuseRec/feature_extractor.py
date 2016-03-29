from __future__ import division
from json import loads as jl
from pickle import dump
from math import log
from itertools import islice

import utility
import config

# Container for user vectors
user_vectors = dict()


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
    sm = {f: {fo: utility.get_cosine_similarity(fv[f], fv[fo]) for fo in funcs if f != fo} for f in funcs}

    return sm


# Update the user vector with each function count.
def update_vector(user_id, func_name, func_count):
    if func_count == 0:
        return

    # Find the user_id and get the corresponding vector.
    vector = user_vectors.get(user_id, dict())

    # Update the vector.
    vector[func_name] = vector.get(func_name, 0) + func_count
    user_vectors[user_id] = vector
    return


# Workhorse function, performs the task of extracting feature vector and the similarity matrix from the json blob.
def process_json_metadata():
    with open(config.fuse["json_file"], 'r') as fd:
        # IMPORTANT: One json record per line, not an array of json objects.
        for line in fd:
            json_record = jl(line)

            # Check if there was an issue with reading the metadata. If this is the case, skip this.
            if json_record["POI"]["problemsWithMetadataAndMacros"] is None:
                continue

            # Find the user identifier, using created by from POI data or the domain name from domain data
            created_by = ""
            last_modified_by = ""
            if "POI" in json_record.keys():
                if json_record["POI"]["createdBy"] is not None:
                    created_by = json_record["POI"]["createdBy"].encode('ascii', 'ignore')
                if json_record["POI"]["lastModifiedBy"] is not None:
                    last_modified_by = json_record["POI"]["lastModifiedBy"].encode('ascii', 'ignore')

            domain_name = ""
            if "InternetDomainName" in json_record.keys() and json_record["InternetDomainName"]["Host"] is not None:
                domain_name = json_record["InternetDomainName"]["Host"].encode('ascii', 'ignore')

            user_id = created_by + "#" + last_modified_by + "#" + domain_name

            for function_key, value in json_record["POI"].iteritems():
                # Check if the key begins with prefix count.
                if function_key.startswith("count"):
                    function_count = int(value)
                    function_name = function_key[len("count"):]

                    if function_count > 0:
                        update_vector(user_id, str(function_name), function_count)

    # Split the vectors into training and testing sets.
    train_size = config.training_data_size
    user_iter = user_vectors.iteritems()

    # Put the training data size amount in the training set, and the rest into testing.
    training_data = dict(islice(user_iter, train_size))
    testing_data = dict(user_iter)

    # Dump the data to a file.
    with open(config.rec_data["training"], "w+") as tr:
        dump(training_data, tr)

    with open(config.rec_data["testing"], "w+") as ts:
        dump(testing_data, ts)

    # Generate the similarity matrix for the training data.
    sm = generate_similarity_matrix(training_data)
    with open(config.rec_data["similarity_matrix"], "w+") as sim:
        dump(sm, sim)

    return


def main():
    process_json_metadata()
    return 0


if __name__ == '__main__':
    main()
