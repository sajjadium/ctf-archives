(*
   RSTcon  -  "Ladder Logic"
   Safety interlock controller, Bay 3 access cabinet.
   Dumped from an OpenPLC runtime. IEC 61131-3 Structured Text.

   The cabinet solenoid (QX0.0) only releases when the engineering keypad
   enters the correct four step combination into the input registers, in
   order, on consecutive scans. When the interlock clears, the controller
   streams the cabinet ID out of the QW output registers.

   Modbus mapping (OpenPLC default):
     %IW0..%IW3  -> input registers 0..3   (keypad steps, operator writes)
     %QW0..%QW19 -> holding registers 0..19 (cabinet ID stream, you read)
     %QX0.0      -> coil 0                  (solenoid)
*)

PROGRAM main
  VAR
    step1 AT %IW0 : WORD;
    step2 AT %IW1 : WORD;
    step3 AT %IW2 : WORD;
    step4 AT %IW3 : WORD;

    solenoid AT %QX0.0 : BOOL;
    id_out AT %QW0 : ARRAY [0..19] OF WORD;

    state : INT := 0;
    unlocked : BOOL := FALSE;
    i : INT;

    (* obfuscated cabinet ID, descrambled only once the interlock clears *)
    KEY : BYTE := 16#5A;
    enc : ARRAY [0..19] OF BYTE := [
        16#28, 16#2F, 16#34, 16#3D, 16#05, 16#6D, 16#05, 16#32,
        16#35, 16#36, 16#3E, 16#29, 16#05, 16#2E, 16#32, 16#3F,
        16#05, 16#31, 16#3F, 16#23 ];
  END_VAR

  (* ---- rung 1: idle, wait for the lead value ---- *)
  IF state = 0 THEN
    IF step1 = 7 THEN
      state := 1;
    END_IF;

  (* ---- rung 2: second tumbler. year the plant opened ---- *)
  ELSIF state = 1 THEN
    IF step2 = 1965 THEN
      state := 2;
    ELSE
      state := 0;
    END_IF;

  (* ---- rung 3: third tumbler. answer to everything ---- *)
  ELSIF state = 2 THEN
    IF step3 = 42 THEN
      state := 3;
    ELSE
      state := 0;
    END_IF;

  (* ---- rung 4: fourth tumbler. 0xCAFE ---- *)
  ELSIF state = 3 THEN
    IF step4 = 16#CAFE THEN
      state := 7;        (* jump straight to the release rung *)
    ELSE
      state := 0;
    END_IF;

  (* ---- rung 7: interlock release. THIS rung holds the key ---- *)
  ELSIF state = 7 THEN
    unlocked := TRUE;
  END_IF;

  (* ---- output stage ---- *)
  solenoid := unlocked;
  IF unlocked THEN
    FOR i := 0 TO 19 DO
      id_out[i] := WORD_TO_INT(enc[i]) XOR WORD_TO_INT(KEY);
    END_FOR;
  ELSE
    FOR i := 0 TO 19 DO
      id_out[i] := 0;
    END_FOR;
  END_IF;

END_PROGRAM

CONFIGURATION Config0
  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#50ms, PRIORITY := 0);
    PROGRAM instance0 WITH task0 : main;
  END_RESOURCE
END_CONFIGURATION
