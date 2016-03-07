from pickle import load as pl

import config


def load_user_vectors():
    vectors = dict()
    with open(config.rec_data["vectors"], "rb") as fd:
        vectors = pl(fd)

    return vectors


def main():
    print load_user_vectors()
    return


if __name__ == "__main__":
    main()
