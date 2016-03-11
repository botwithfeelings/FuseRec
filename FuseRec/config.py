# The json file containing meta data can be found here:
# http://static.barik.net/fuse/fuse-bin.analysis.dedup.poi-dec2014.json.gz
# Extract and set the json_file value to point to the file.
fuse = dict(
    json_file="./Fuse_Data/fuse-bin"
)

# File for dumping pickle data.
rec_data = dict(
    vectors="./Fuse_Data/user_vectors",
    vectors_weighted="./Fuse_Data/user_vectors_weighted",
    similarity_matrix="./Fuse_Data/similarity_matrix"
)

pickle_dump_weighted = True

# Tuning params throughout the system.
tuning_param = dict(
    alpha=10,
    expected_freq_weight=10,
    num_sims=10,
    num_recs=5
)
