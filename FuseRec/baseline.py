import utility
import config

from random import choice
from state import *


# Get recommendations for user, where the functions are in the most popular list but not in the user's list.
def get_recommendations(mp, data):
    recs = [f for f in mp if f not in data.keys()]

    if len(recs) > config.tuning_param["num_recs"]:
        recs = recs[0: config.tuning_param["num_recs"]]

    return recs


def do_most_popular(train, test):
    success = 0

    # Generate the similarity matrix for the given data.
    mp = utility.generate_most_popular_list(train)

    for data in test.itervalues():
        # The function to be removed.
        test_func = choice(data.keys())
        data.pop(test_func)

        # Get the recommendation for the user in training data.
        if test_func in get_recommendations(mp, data):
            success += 1

    return success


def do_cv():
    # Load the user vectors.
    data = utility.load_vectors()
    outfile_string = "baseline_slice" + str(config.num_slices) \
                     + "_rec" + str(config.tuning_param['num_recs']) + ".txt"
    rates = list()
    st = state('Item Based', rates, outfile_string, "INFO", config.num_slices, config.tuning_param['num_recs'])
    for i in xrange(st.num_slices):
        st.cur_slice += 1
        train, test = utility.get_data_split(data, i)
        success = do_most_popular(train, test)
        st.rates = (success, len(test))
    return st


def main():
    final_state = do_cv()
    print(final_state)
    final_state.term()
    return


if __name__ == "__main__":
    main()
