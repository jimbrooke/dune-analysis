import numpy as np
import awkward

class ClusterVars():
    def __init__(self, name, out_dir, collection='marley', mask=None, out_var=None):
        self.name = name
        self.out_dir = out_dir
        self.mask = mask
        self.branches = ['Hit_True_GenType', 'Hit_True_MarleyIndex', 'Hit_Size', 'Hit_Start_Tick'] #this line simplified a lot
        if out_var:
            self.out_var = out_var
        else:
            self.out_var = 'DeltaStart'

    def event(self, chunk):

        Hit_True_GenType, Hit_True_MarleyIndex, Hit_Size, Hit_Start_Tick = chunk.tree.arrays(self.branches, outputtype=tuple)

        # mask to get the hits we care about
        mask1 = Hit_True_GenType==1
        mask2 = Hit_True_MarleyIndex==0
        mask = np.logical_and(mask1, mask2)

        hit_start = Hit_Start_Tick[mask]

        # only select events with at least two hits in the mask
        has_two_hits = Hit_Start_Tick[mask].counts > 1

        # default output is np.inf
        out = np.full(len(chunk.tree), np.inf)

        # calculate max-min
        start_max = hit_start[has_two_hits].max()
        start_min = hit_start[has_two_hits].min()

        out[has_two_hits] = start_max - start_min

        chunk.tree.new_variable(self.out_var, out)
        return True


class ClusterFinder():
    def __init__(self, name, out_dir, mask=None, out_var=None):
        self.name = name
        self.out_dir = out_dir
        self.mask = mask
        self.branches = ['Hit_Chan', 'Hit_Size', 'Hit_Start_Tick'] #this line simplified a lot
        if out_var:
            self.out_var = out_var
        else:
            self.out_var = 'clusterNHits'

    def event(self, chunk):

        # get the data
        Hit_Chan, Hit_Start_Tick = chunk.tree.arrays(['Hit_Chan', 'Hit_Start_Tick'], outputtype=tuple)

        # apply a mask if required
        if self.mask:
            mask = chunk.tree.array(self.mask)
            Hit_Chan = Hit_Chan[mask]
            Hit_Start_Tick = Hit_Start_Tick[mask]

        clusterNHits = []

        # loop over events
        for chans, starts in zip(Hit_Chan, Hit_Start_Tick):

            # channels with hits in this event
            print("Hit channels : ",chans)

            # find the clusters
            clusters = np.split(chans, np.where(np.diff(chans) != 1)[0]+1)
            
            # this will store a variable for each cluster
            n_hits_per_clus = []

            # loop over clusters
            for i, clus in zip(range(len(clusters)),clusters):
                print(i, clus)
                n_hits_per_clus.append(len(clus))
            
            # add the list of cluster variables to the output list
            clusterNHits.append(n_hits_per_clus)

        # store the new cluster variable in the event
        chunk.tree.new_variable(self.out_var, awkward.fromiter(clusterNHits))

        return True
