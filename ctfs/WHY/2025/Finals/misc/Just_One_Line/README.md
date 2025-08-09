What would a CTF be without a perl one-liner:
$ echo ${FLAG} | perl -ple '$n=()=/./g;$_=~s/./$|--?ord($&)%$n:ord($&)-$^F**5/eg'
