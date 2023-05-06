import byte_analizer as ba

with open("bcode.lbc", "r") as fi:
  statmts = fi.read().split("\n")
  for i in statmts:
    ba.analize(i)