This old floor cleaning bot ate my flag! Its one of those old models with an obscure language chip installed, which is only made worse by its sluggish response times. I'm losing my patience!

from pwn import *
p = remote("spaceheroes-patient-robot.chals.io", 443, ssl=True, sni="spaceheroes-patient-robot.chals.io")
p.interactive()

md5sum: cb8531bfe27ab82366d19883f5296a2f PatientRobot
