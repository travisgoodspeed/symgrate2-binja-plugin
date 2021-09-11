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

def jprint(j):
    """Prints the results from JSON."""
    # Parse the JSON.
    x=json.loads(j)

    #Print each name and record.
    for f in x:
        print(f, x[f]["Name"])

def dumpfile(f):
    """Dumps all the symgrate-identifiable symbols in a .bndb file."""
    global bv
    bv = binaryninja.open_view(f)

    if bv==None:
        print("Failed to load %s."%f);
        return;
    
    # This is the gross architecture, but individual functions might have
    # different architectures.  arm7/thumb2, for example.
    print("Loaded %s for architecture %s."%(f, bv.arch));
    
    count=0;
    q="";
    for f in bv.functions:
        pre=functionprefix(f);
        count=count+1;
        
        q+=("%08x=%s&"%(f.start, pre));
        
        if count&0x3F==0x00:
            res=Symgrate2.queryjfns(q);
            q="";
            if res!=None: jprint(res);
    res=Symgrate2.queryjfns(q);
    if res!=None: jprint(res);
            

if len(sys.argv)==1:
    print("Usage: %s foo.bndb"%sys.argv[0]);
else:
    for f in sys.argv[1:]:
        print("Querying %s"%f);
        dumpfile(f);


