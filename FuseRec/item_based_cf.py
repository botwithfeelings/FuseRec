from __future__ import division

import utility
import config


# Globals for similarity matrix and user vectors.
sm = dict()
uv = dict()


def get_average(l):
    return sum(l)/len(l)


def get_recommendations(user):
    # Get the list of functions used by the user
    user_funcs = list(uv[user].keys())

    # Get similarity scores - mean of similarity values of functions used by the user,
    # in the similarity vector for functions not used by the user.
    sim_scores = {f: get_average([v for (fo, v) in sm[f].iteritems() if fo in user_funcs])
                  for f in sm.iterkeys() if f not in user_funcs}

    # Sort by the scores.
    recs = sorted(sim_scores, key=sim_scores.get, reverse=True)

    return recs[0: config.tuning_param["num_recs"]]


def do_item_cf():
    # TODO handle user input vector here.
    recommendations = {user: get_recommendations(user) for user in uv.iterkeys()}

    # Temporary view.
    print recommendations

    # TODO insert cross validation code here.
    return


def main():
    global sm, uv
    sm, uv = utility.load_sim_matrix(), utility.load_vectors(False)
    do_item_cf()
    return


if __name__ == "__main__":
    main()
