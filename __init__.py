#!/usr/bin/env python3

from binaryninja import *

import sys, json

from .Symgrate2 import Symgrate2

LEN = 18
BATCHSIZE = 0x3f

def functionprefix(bv,fun):
    """Returns the first LEN bytes of a function as ASCII."""
    B=bv.read(fun.start, LEN)
    
    if len(B)!=LEN:
        return ""
        
    #https://api.binary.ninja/binaryninja.transform.Transform.html#binaryninja.transform.Transform
    #Only gotcha is you have to decode as utf8 to get str instead of bytearray
    rawhex=Transform['RawHex']
    return rawhex.encode(B).decode('utf8')


def function_search(bv,f):
    """Searches for one function."""
    count=0
    pre=functionprefix(bv,f)
    name=Symgrate2.queryfn(pre)

    if name!=None:
        if f.symbol.auto: #built-in symbol we can likely overwrite
            f.name = name.strip()
            show_message_box("Symgrate2 Query", "Found name: %s." % f.name,
                            MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)
        else:
            show_message_box("Symgrate2 Query", "Identified as %s, but existing user name is %s so not auto-setting."% (name, f.name),
                            MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)
    else:
        show_message_box("Symgrate2 Query", "Unknown function.",
                         MessageBoxButtonSet.OKButtonSet, MessageBoxIcon.ErrorIcon)


def allfunction_searchbg(bv):
    """Searches for all functions in the background."""
    # Start a solver thread for the path associated with the view
    s = Solver(bv)
    s.start()

def parse_results(bv, j):
    """Parses a JSON bundle from the server."""
    count=0
    x=json.loads(j)
    for f in x:
        adr=int(f,16)
        name=x[f]["Name"]
        F=bv.get_function_at(adr)  # Binja's view of the same function.

        # Print the name and log the result.
        if F.symbol.auto: # Built-in symbol we can overwrite.
            F.name=name # Overwrite the name.
            log_info("Symgrate2: %s %s" % (f, name))
        elif F.name==name:
            # The name has already been set, so don't bother printing it in results.
            pass;
        else:
            # The name disagrees.  Print both.
            log_info("Symgrate2: %s %s!=%s" % (f, name, F.name))
        count=count+1;

        # Update the name, if appropriate.
    return count;

def parse_result(bv, line):
    line=line.strip()
    if line == "":
        return 0
    try:
        (offset, fname) = line.split(" ", 1)
    except:
        log_warn("Symgrate2: Result %s not valid." % line)
        return 0

    offset = int(offset, 16)
    f = bv.get_function_at(offset)
    if f:
        if f.symbol.auto: #built-in symbol we can likely overwrite
            f.name = fname
            log_debug("Symgrate2: Setting function name at 0x%x to %s" % (f.start, f.name))
        else:
            log_warn("Symgrate2: Function %s at 0x%x was already named by the user, refusing to override with Symgrate2 result: %s" % (f.name, f.start, line.strip()))
        return 1
    else:
        return 0

class Solver(BackgroundTaskThread):
    def __init__(self, bv):
        BackgroundTaskThread.__init__(self, "Searching Symgrate2", True)
        self.bv=bv
    def run(self):
        """Searches for all functions."""
        count=0
        matches=0
        bv=self.bv

        count=0
        q={}
        for f in bv.functions:
            pre=functionprefix(self.bv,f)
            count=count+1

            q["%08x" % f.start] = pre

            if count&BATCHSIZE==0:
                self.progress=("Symgrate2: Searched %d functions" %(count))
                res=Symgrate2.queryjfns(q)
                q={}
                if res!=None:
                    matches += parse_results(bv, res)
        self.progress=("Symgrate2: Searched %d functions" %(count))
        res=Symgrate2.queryjfns(q)
        if res!=None:
            matches += parse_results(bv, res)
        log_info("Symgrate2: Searched %d functions and found %d matches." % (count, matches))

PluginCommand.register_for_function("Symgrate2 Function Search", "Searches Symgrate2 db for the current function.", function_search)
PluginCommand.register("Symgrate2 Program Search", "Searches Symgrate2 db for all functions.", allfunction_searchbg)
