import numpy as np

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
