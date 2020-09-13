#!/usr/bin/env python3

from binaryninja import *

import sys;

from .Symgrate2 import Symgrate2

LEN = 18;

def functionprefix(bv,fun):
        """Returns the first eighteen bytes of a function as ASCII."""
        B=bv.read(fun.start, LEN);
        raw="";
        for i in range(0, LEN, 2):
                h=int(B[i+1]);
                l=int(B[i]);
                raw+="%02x%02x"%(l,h);
        #print("raw:     %s"%raw);
        return raw;


def function_search(bv,f):
        """Searches for one function."""
        count=0;
        pre=functionprefix(bv,f);
        name=Symgrate2.queryfn(pre);

        if name!=None:
                show_message_box("Symgrate2 Query", "Identified as %s."%name,
                                 MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)
        else:
                show_message_box("Symgrate2 Query", "Unknown function.",
                                 MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)


def allfunction_searchbg(bv):
        """Searches for all functions in the background."""
        # Start a solver thread for the path associated with the view
        s = Solver(bv)
        s.start()


class Solver(BackgroundTaskThread):
        def __init__(self, bv):
                BackgroundTaskThread.__init__(self, "Searching Symgrate2.", True);
                self.bv=bv;
        def run(self):
                """Searches for all functions."""
                count=0;
                matches=0;
                bv=self.bv;
                
                for f in bv.functions:
                        pre=functionprefix(bv,f);
                        name=Symgrate2.queryfn(pre);

                        count=count+1;
                        if name!=None:
                                #print("found %s"%name);
                                print("%08x %-20s" % (f.start, name));
                                matches=matches+1;
                        self.progress=("Searched %d functions on Symgrate2, %d matches." %(count,matches))

        
PluginCommand.register_for_function("Symgrate2 Function Search", "Searches Symgrate2 db for the current function.", function_search)
PluginCommand.register("Symgrate2 Program Search", "Searches Symgrate2 db for all functions.", allfunction_searchbg)


