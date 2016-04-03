# The json file containing meta data can be found here:
# http://static.barik.net/fuse/fuse-bin.analysis.dedup.poi-dec2014.json.gz
# Extract and set the json_file value to point to the file.
json_data="./Fuse_Data/fuse-bin"

# File for dumping pickle data.
user_data = "./Fuse_Data/data.dat"

# No of slices for user data.
num_slices = 14

# Tuning params throughout the system.
tuning_param = dict(
    alpha=10,
    expected_freq_weight=10,
    num_sims=10,
    num_recs=10
)
