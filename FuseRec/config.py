# The json file containing meta data can be found here:
# http://static.barik.net/fuse/fuse-bin.analysis.dedup.poi-dec2014.json.gz
# Extract and set the json_file value to point to the file.
fuse = dict(
    json_file="./Fuse_Data/fuse-bin"
)

# File for dumping pickle data.
rec_data = dict(
    vectors="./Fuse_Data/user_vectors"
)

# Tuning params throughout the system.
tuning_param = dict(
    alpha=1
)
