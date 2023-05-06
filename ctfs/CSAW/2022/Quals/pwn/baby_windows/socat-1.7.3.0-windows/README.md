Since no one else has compiled socat for windows, here it is.

I used some optimizations, which should help this version of socat stand 
out from the rest.

Those optimizations were -march=i586 -flto -fomit-frame-pointer

I didn't want to get too crazy, since that sometimes leads to weird 
issues.
