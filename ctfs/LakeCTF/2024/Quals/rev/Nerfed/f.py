class F:
 def __init__(s)->None:
  s.__flag=0
 def x(s,bit):
  s.__flag= s.__flag^(1<<bit)
 def s(s,bit,value=1):
  if value!=s.gf(bit):
   s.x(bit)
 def c(s,bit):
  s.__flag=s.__flag&~(1<<bit)
 def gf(s,bit):
  return 1 if s.__flag&(1<<bit)else 0
 def gh(s):
  return hash(s.__flag)
 def gn(s):
  return s.__flag
# Created by pyminifier (https://github.com/liftoff/pyminifier)
