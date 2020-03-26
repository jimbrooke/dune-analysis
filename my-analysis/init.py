import numpy as np
class MarleyCount():
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
        if self.mask:
            mask = chunk.tree.array(self.mask)
            Hit_True_GenType = Hit_True_GenType[mask]
            Hit_True_MarleyIndex = Hit_True_MarleyIndex[mask]
            Hit_Size = Hit_Size[mask]
        Delta_Start = []
        a = np.amin(Hit_Start_Tick[Hit_True_MarleyIndex == 0])
        b = np.amax(Hit_Start_Tick[Hit_True_MarleyIndex == 0])
        Delta_Start = b - a 
        chunk.tree.new_variable(self.out_var, Delta_Start)
        return True
