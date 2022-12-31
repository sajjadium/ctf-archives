[REDACTED]

#ifndef W
#define W
#include <stdio.h>
typedef unsigned int _;_ J[]={
#include __FILE__
#undef W
0},G,F,l[256],I[256],A,y,m,D,e,R,h;_*w(){if(!G--){y+=++m;for(h=0;h<256;y=l[h++]
=I[255&(R>>10)]+e){A^=(h&1)?A>>((h&2)?16:6):A<<((h&2)?2:13);e=I[h];R=I[h]=I[255
&(e>>2)]+(A+=I[(h+128)&255])+y;}G=255;}return&l[G];}_*X(){for(F=0;256>F;I[F++]=
0);for(F=0;sizeof(J)/sizeof(_)>F;F++)I[F&255]^=J[F];for(A=y=m=G=F=0;F<1<<24;++F
)w();D=F=0x0;return&F;}char*S,s[]="ASIS{7_i<gSp@KuKbW=y5A+@S@'KW2Z_|Gzk3`<liC2"
"yR6pyn=nTAC})qb?pSVt0oC~iAp@*e/Y*OTUJVD{8A&CpFp2E26}IKXAVrQ|3Xx~sOloFS<,Uu@Bv"
"qWa9xcNv=6Q<T}*a3=u(VfNz/gPMbAl!~^qii{i{k]``_br]zjhampxi|hjao~qmmat{pxyylwsl_"
"p~{]e";main(){X();for(S=s+*J;*S>37;){for(h=0;h<5;h++){D*=85;D+=(*S++-6)%89;};D
^=*w();for(h=0;h<4;h++){s[F++]=D&255;D>>=8;}}return!fwrite(s,F-*S%5,1,stdout);}
#endif
