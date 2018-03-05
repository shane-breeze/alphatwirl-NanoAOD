import os
import random
import datetime
import array

#from rootpy.tree import Tree
#from rootpy.io import root_open
import ROOT

class SaveTree(object):
    """
    Reader to save the contents of an event into a TTree. Creates a "snapshot"
    of the event for faster processing
    """
    __typedic = dict(
        c = 'C',
        b = 'B',
        B = 'b',
        h = 'S',
        H = 's',
        i = 'I',
        I = 'i',
        f = 'F',
        d = 'D',
        l = 'L',
        L = 'l',
    )

    def __init__(self, outdir, file_name=None, tree_name="Events",
                 branch_type_pairs=[
                     ("isdata","i"),
                     ("comp_name","c"),
                     ("comp_era","c"),
                     ("comp_nevents","i"),
                     ("cross_section","f"),
                 ],
                ):
        self.outdir = outdir
        self.file_name = file_name
        self.tree_name = tree_name
        self.branch_type_pairs = branch_type_pairs

    def begin(self, event):
        # Give root file a random name
        if self.file_name == None:
            self.file_name = "{}_{:06x}.root".format(
                datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
                random.getrandbits(6*4), # 6 digits in hex
            )

        outdir = os.path.join(
            self.outdir,
            event.component.dataset,
            event.component.era,
        )
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        outpath = os.path.join(outdir, self.file_name)
        self.file_path = outpath

        # Copy all branches to the new tree
        # TODO: Add additional branches created during runtime
        event.tree.SetBranchStatus('*',1)
        self.f_copy = ROOT.TFile.Open(outpath, 'recreate')
        self.f_copy.cd()
        self.t_copy = event.tree.CloneTree(0)

        for attr, typecode in self.branch_type_pairs:
            attr_val = array.array(typecode, getattr(event, attr))
            setattr(self, attr, attr_val)
            if typecode != "c":
                self.t_copy.Branch(attr, attr_val, "{}/{}".format(attr, self.__typedic[typecode]))
            else:
                self.t_copy.Branch(attr, attr_val, "{}[{}]/{}".format(attr, len(attr), self.__typedic[typecode]))

        event.tree.CopyAddresses(self.t_copy)

    def event(self, event):
        self.t_copy.Fill()

    def end(self):
        self.f_copy.cd()
        self.t_copy.Write()
        self.f_copy.Close()

        # Delete attributes. When we close f_copy, t_copy goes bye bye and
        # becomes an object of type PyROOT_NoneType which can't be pickled to
        # store the result. Doesn't matter though because we're already writing
        # the result to a root file
        del self.t_copy
        del self.f_copy
