# The json file containing meta data can be found here:
# http://static.barik.net/fuse/fuse-bin.analysis.dedup.poi-dec2014.json.gz
# Extract and set the json_file value to point to the file.
fuse = dict(
    json_file="./Fuse_Data/fuse-bin"
)

# File for dumping pickle data.
rec_data = dict(
    training="./Fuse_Data/training.dat",
    testing="./Fuse_Data/testing.dat",
    similarity_matrix="./Fuse_Data/similarity_matrix.dat"
)

# Percent of total user vectors to be used for training.
training_data_size = 0.7

# No. of times the cross validation should be run.
cv_runs = 5

# Tuning params throughout the system.
tuning_param = dict(
    alpha=10,
    expected_freq_weight=10,
    num_sims=10,
    num_recs=5
)
