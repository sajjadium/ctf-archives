#!/usr/bin/env python3
import random
import PIL.Image
import numpy as np
from PIL import Image
import pickle
import secrets
from m import M
from r import R
from t import T
from f import F
def fin():
 fl.c(0)
 exit("congrats, you can get flag")
def fl_s():
 fl.s(1,tb.c_c[rs.g(0),rs.g(1)])
 fl.s(13,tb.r_c[rs.g(0),rs.g(1)])
 fl.s(14,tb.f_c[rs.g(0),rs.g(1)])
def com(instr):
 if fl.gf(2):
  return
 cur_h=hash((tuple(rs.gh()),fl.gh(),tuple(me.gh().tolist())))
 if cur_h==tb.c_h[rs.g(0),rs.g(1)]:
  me.s()
  try:
   instr=instr[rs.g(1)+1:]
  except IndexError:
   fl.s(2)
   rs.s(10,69)
  rs.s(tb.r_s[rs.g(0)][0],tb.r_s[rs.g(0)][1])
  rs.s(0,1+rs.g(0))
  rs.s(1,0)
 else:
  fl.s(2)
 return instr
def fl_c():
 cur_num=fl.gn()
 if cur_num!=tb.f_h[rs.g(0),rs.g(1)]:
  fl.s(2)
def r_c():
 cur_h=rs.gh()
 if cur_h!=tb.r_h[rs.g(0),rs.g(1)].tolist():
  fl.s(2)
def e_c():
 if rs.g(10):
  fl.s(2)
def start():
 if rs.g(0)+rs.g(1)!=0:
  fl.s(2)
 else:
  fl.s(0)
  fl.s(1)
def rt():
 fl.c(3)
 fl.x(4)
 fl.c(5)
 fl.c(6)
 fl.c(7)
 fl.c(8)
 fl.c(9)
 fl.c(10)
 fl.c(11)
 fl.c(12)
 fl.c(13)
 fl.c(14)
 fl.c(15)
 rs.s(6,0)
 rs.s(7,0)
 rs.s(8,0)
 rs.s(9,0)
 rs.s(10,0)
def g_t():
 try:
  if rs.g(rs.g(3))<rs.g(rs.g(4)):
   fl.s(12)
 except IndexError:
  fl.s(2)
def l_i(ins):
 rs.s(5,ord(ins))
 fl.s(3)
 fl.x(5)
def c_i():
 fl.s(1)
 fl.x(6)
def incr(ins):
 rs.s(ord(ins)-9,1+rs.g(ord(ins)-9))
 fl.x(7)
def ma(src,dst):
 rs.s(dst,rs.g(src))
 fl.x(11)
def andd(ins):
 try:
  rs.s(rs.g(5),rs.g(rs.g(4))&rs.g(ord(ins)-0x20))
 except IndexError:
  fl.s(2)
def xor(ins):
 try:
  rs.s(ord(ins)-0x28,rs.g(rs.g(3))^rs.g(rs.g(4)))
 except IndexError:
  fl.s(2)
def f_t_r(ins):
 rs.s(ord(ins)-0x30,fl.gn())
 fl.x(10)
def ad(ins):
 try:
  rs.s(ord(ins)-0x38,rs.g(rs.g(3))+rs.g(rs.g(4)))
 except IndexError:
  fl.s(2)
 fl.x(8)
def l_m(ins):
 me.m(tb.masks[ord(ins)-0x01],37*rs.g(2)+rs.g(1))
 fl.x(15) 
inss=input("What's up ('til newline ofc)? ")
if __name__=="__main__":
 fl=F()
 me=M()
 tb=T()
 rs=R()
 while True:
  if fl.gf(2):
   exit()
  if rs.g(0)==11:
   fin()
  fl_s()
  try:
   ins=inss[rs.g(1)]
  except IndexError:
   fl.s(2)
  if ins=="\x00" and not fl.gf(2):
   start()
  elif fl.gf(3)and fl.gf(0)and not fl.gf(2):
   rs.s(rs.g(5),ord(ins))
   fl.c(3)
  elif fl.gf(0)and not fl.gf(2):
   match ins:
    case "\x1d":
     ma(7,10)
    case "\x01":
     rt()
    case "\x17":
     ma(4,5)
    case "\x1a":
     ma(8,5)
    case "\x02":
     g_t()
    case "\x15":
     ma(3,4)
    case "\x16":
     ma(4,2)
    case ins if ord(ins)<11:
     l_i(ins)
    case "\x19":
     ma(6,4)
    case "\x18":
     ma(5,7)
    case ins if ord(ins)<0x13:
     incr(ins)
    case "\x13":
     ma(0,8)
    case "\x1b":
     ma(8,10)
    case "\x1c":
     ma(7,2)
    case "\x14":
     ma(0,4)
    case "\x1e":
     ma(9,3)
    case "\x1f":
     ma(10,8)
    case ins if ord(ins)<0x2a:
     andd(ins)
    case ins if ord(ins)<0x32:
     xor(ins)
    case ins if ord(ins)<0x3a:
     f_t_r(ins)
    case ins if ord(ins)<0x42:
     ad(ins)
    case ins if ord(ins)<253:
     l_m(ins)
    case "\xff":
     c_i()
    case _:
     fl.s(2)
  else:
   exit("3735928559")
  e_c()
  if fl.gf(13):
   r_c()
  if fl.gf(14):
   fl_c()
  e_c()
  if fl.gf(1):
   inss=com(inss)
  else:
   rs.s(1,1+rs.g(1))
  e_c()
# Created by pyminifier (https://github.com/liftoff/pyminifier)
