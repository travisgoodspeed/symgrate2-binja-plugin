from binaryninja import *

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

def allfunction_search(bv):
        """Searches for all functions."""
        count=0;

        for f in bv.functions:
                pre=functionprefix(bv,f);
                name=Symgrate2.queryfn(pre);

                if name!=None:
                        print("found %s"%name);
                else:
                        print("Missing %s"%pre);

PluginCommand.register_for_function("Symgrate2 Function Search", "Searches Symgrate2 db for the current function.", function_search)
PluginCommand.register("Symgrate2 Program Search", "Searches Symgrate2 db for all functions.", allfunction_search)


