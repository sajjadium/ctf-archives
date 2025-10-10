BY	xtea418
TAGS	web
Guten Morgen,
Sie sind seit heute für unseren online shop von unserem Plfanzen Laden verantwortlich...
Der sollte eigentlich funktionieren 🙏🙏🙏
Das Deployment haben wir extern eingekauft, deswegen ist das so fancy... startet sich sogar selber neu wenn des ding down geht... und so
Wegen einem Sicherheitsvorfall haben wir die Review Funktion abgeschaltet (oder so...), damit da niemand mehr sachen mit machen kann.
Es ist stark empfohlen diesen Task zuerst lokal zu öffen. 🍉
You get a host to run your exploit from, copy the
ncat --ssl <domain> 31337 command and then export COMMAND='ncat --ssl <domain> 31337', to ssh:

ssh -o "ProxyCommand=$COMMAND" root@localhost

to scp:

scp -o "ProxyCommand=$COMMAND" -r ./challenge-solution/ root@localhost:

the creds for that host are root:meowmeowmeowmeowmeowmeow
