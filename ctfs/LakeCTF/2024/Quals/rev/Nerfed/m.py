#!/usr/bin/env python3
import numpy as np
class M:
 def __init__(s)->None:
  s.__m=np.load("flag.npz")["flag"]
 def gh(s):
  x_m=np.zeros(s.__m.shape[1],dtype=np.int8)
  for i in range(s.__m.shape[0]):
   x_m=x_m^s.__m[i]
  x_m.flags.writeable=False
  return x_m
 def s(s):
  mask=s.gh()*np.ones(s.__m.shape,dtype=np.int8)
  s.__m=s.__m^mask
 def m(s,mask,offset):
  s.__m=s.__m^ np.roll(mask,offset,axis=1)
 def w(s):
  return s.__m
# Created by pyminifier (https://github.com/liftoff/pyminifier)
