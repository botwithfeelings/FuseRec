# Project Source for CSC 791 (Spring 16): Machine Learning for User Adaptive Systems

## Running the system

#### Item Based Collaborative Filtering

This is run by a simple command:

``` 
python item_based_cf.py
```

The main parameters for the algorithm can be configured in config.py.  The most important of these are:

- num_slices:  This determines the number of folds to use for K-Folds crossvalidation.

- num_recs:  This determines the number of recommendations returned by the algorithm.  In test cases if the removed test function is in the the list of recomendations, then we count that test as a success.  Essentially, decreasing the number of recommendations increases the difficulty.

The logger is setup to return outfiles into a directory called ./FuseRec/out.  The files themselves are in the following format:

```
<algoname>_slice<slice_number>_rec<number_of_recommendations>.txt
```

All of those parameters are filled in by the actual algorithm chosen and the configuration parameters from config.py.  One important thing to take note of: If you run a particular setup that has been run before (For example, anything setup that is in the out directory) the original log of that run type will be deleted and written over.  The main reasoning for this is that the python logger is setup to append to these outfiles.  For our purposes that is suboptimal.