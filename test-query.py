#!/usr/bin/env python3

from binaryninja import *

from Symgrate2 import Symgrate2

samples=["0a460346024908681946fff7b9bf00bfc400"];

for sample in samples:
    res=Symgrate2.queryfn(sample);
    if res!=None:
        print("%10s %s"%(res,sample));

