#!/usr/bin/env python3

from binaryninja import *

import sys;

from Symgrate2 import Symgrate2

bv=None;
LEN = 18;

def functionprefix(fun):
    """Returns the first eighteen bytes of a function as ASCII."""
    B=bv.read(fun.start, LEN);
    raw="";
    for i in range(0, LEN, 2):
        h=int(B[i+1]);
        l=int(B[i]);
        raw+="%02x%02x"%(l,h);
    #print("raw:     %s"%raw);
    return raw;


def dumpfile(f):
    """Import a .o file to the database."""
    global bv
    bv = binaryninja.open_view(f)

    if bv==None:
        print("Failed to load %s."%f);
        return;
    
    # This is the gross architecture, but individual functions might have
    # different architectures.  arm7/thumb2, for example.
    print("Loaded %s for architecture %s."%(f, bv.arch));
    
    ## Print the recovered name of each function.
    for f in bv.functions:
        pre=functionprefix(f);
        name=Symgrate2.queryfn(pre);
        if name!=None:
            sys.stdout.write("\n%08x %-20s" % (f.start, name));
        else:
            sys.stdout.write(".");
            sys.stdout.flush();
    sys.stdout.write("\n");

if len(sys.argv)==1:
    print("Usage: %s foo.bndb"%sys.argv[0]);
else:
    for f in sys.argv[1:]:
        print("Querying %s"%f);
        dumpfile(f);


