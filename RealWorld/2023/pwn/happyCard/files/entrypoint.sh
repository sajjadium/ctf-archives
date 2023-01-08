JC_HOME_TOOLS=/java_card_tools/
JC_HOME_SIM=/wine/drive_c/Program\ Files/Oracle/Java\ Card\ Development\ Kit\ Simulator\ 3.1.0/

SIM_CP=$JC_HOME_TOOLS/lib/asm-8.0.1.jar:$JC_HOME_TOOLS/lib/commons-cli-1.4.jar:$JC_HOME_TOOLS/lib/commons-logging-1.2-9f99a00.jar:$JC_HOME_TOOLS/lib/json.jar:$JC_HOME_TOOLS/lib/tools.jar:$JC_HOME_SIM/lib/jctasks_simulator.jar:$JC_HOME_SIM/lib/tools_simulator.jar:$JC_HOME_SIM/lib/api_classic.jar:$JC_HOME_SIM/lib/api_classic_annotations.jar
TOOLS_CP=$JC_HOME_TOOLS/lib/asm-8.0.1.jar:$JC_HOME_TOOLS/lib/commons-cli-1.4.jar:$JC_HOME_TOOLS/lib/commons-logging-1.2-9f99a00.jar:$JC_HOME_TOOLS/lib/jctasks_tools.jar:$JC_HOME_TOOLS/lib/json.jar:$JC_HOME_TOOLS/lib/tools.jar:$JC_HOME_TOOLS/lib/api_classic-3.1.0.jar:$JC_HOME_TOOLS/lib/api_classic_annotations-3.1.0.jar

verifycap() {
	java -Djc.home="$JC_HOME_TOOLS" -classpath "$TOOLS_CP" com.sun.javacard.offcardverifier.Verifier -nobanner $@
}

scriptgen() {
	java -Djc.home="$JC_HOME_SIM" -classpath "$SIM_CP" com.sun.javacard.scriptgen.Main -nobanner $@
}

script=/tmp/script

verifycap -outfile /tmp/hello.cap.digest /files/hello.cap
scriptgen -hashfile /tmp/hello.cap.digest -o /tmp/hello.cap.script /files/hello.cap
cat << EOF > $script
powerup;
output off;
0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F;
EOF
FLAG=`echo -n "$FLAG"|perl -lne 'print map {"0x".(unpack "H*",$_)." "} split //, $_;'`
cat /tmp/hello.cap.script >> $script
cat << EOF >> $script
0x80 0xB8 0x00 0x00 0x08 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xAA 0x00 0x7F;
0x00 0xA4 0x04 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xAA 0x7F;
0x88 0x88 0x00 0x00 0x30 $FLAG 0x7f;
0x00 0xA4 0x04 0x00 0x09 0xA0 0x00 0x00 0x00 0x62 0x03 0x01 0x08 0x01 0x7F;
EOF

TMPDIR=/jctmp
mkdir $TMPDIR
cd /upload
for capfile in *.cap; do
    [ -f "$capfile" ] || continue
	verifycap -outfile "$TMPDIR/$capfile.digest" /upload/*.exp "$capfile" || { echo "verify failed"; exit; }
	scriptgen -hashfile "$TMPDIR/$capfile.digest" -o "$TMPDIR/$capfile.script" "$capfile" || { echo "scriptgen failed"; exit; }
	cat "$TMPDIR/$capfile.script" >> /tmp/script
done
echo "All verification finished"

cat << EOF >> $script
0x80 0xB8 0x00 0x00 0x08 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF 0x00 0x7F;
0x00 0xA4 0x04 0x00 0x06 0xAA 0xBB 0xCC 0xDD 0xEE 0xFF 0x7F;
output on;
0x88 0x66 0x00 0x00 0x00 0x7f;
EOF

wine 'C:\Program Files\Oracle\Java Card Development Kit Simulator 3.1.0\bin\cref_t1.exe' -nobanner -nomeminfo &
sleep 5
java -Djc.home="$JC_HOME_SIM" -classpath "$SIM_CP" com.sun.javacard.apdutool.Main -nobanner -noatr $script
