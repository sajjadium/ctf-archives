! Copyright (C) 2023 Robin Jadoul.
! See https://factorcode.org/license.txt for BSD license.
USING: kernel io io.encodings.utf8 io.files math math.matrices namespaces prettyprint random sequences vectors ;
IN: ictf.flagtor

: mask-value ( -- n ) [ random-32 -24 shift ] with-secure-random ; inline
: sample-mask ( n -- v ) V{ } [ dup length pick < dup [ mask-value pick push ] when ] loop nip ;
: crypt ( v v -- v ) [ bitxor ] 2map ;
: read-flag ( -- v ) "flag.txt" utf8 file-lines first ;
: with-seed ( ... n quot -- ... ) swap random-generator get swap seed-random swap with-random ; inline
: into-matrix ( v -- m ) dup length dup [ 2drop dup random random-32 -24 shift * ] <matrix-by-indices> nip ;
: with-1 ( v -- v ) clone dup 1 swap push ; inline
: round ( n v v -- n v ) pick [ with-1 dup into-matrix vdotm [ 257 mod ] map . ] with-seed ;
: first-round ( v -- v ) dup length sample-mask 2dup crypt >vector . 0 -rot round nip ;
: other-round ( n v -- n v ) [ 1 + ] dip dup length sample-mask round ;

: main ( -- ) read-flag first-round 0 swap dup length 26 - [ other-round ] times 2drop ;

MAIN: main
