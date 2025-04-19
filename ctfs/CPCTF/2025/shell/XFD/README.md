In Excel 2007 and later versions, there are 16,384 columns, and the columns are named in alphabetical order: A, B, C..., Y, Z, AA, AB... ZY, ZZ, AAA, AAB... XFC, XFD. Create a text file like the one below
, with all of these column names (A to XFD) delimited by line breaks (\n).

A
B
C
...
Y
Z
AA
AB
...
AY
AZ
BA
BB
...
ZY
ZZ
AAA
AAB
...
AAY
AAZ
ABA
ABB
...
AZY
AZZ
BAA
BAB
...
XFC
XFD

The XFD must also be immediately followed by exactly one newline (\n).

The flag to submit is CPCTF{SHA256 hash of the file above}.
For example, if the resulting text file looks like this, columns A through C:

A
B
C

If so, the flag to submit CPCTF{706204f15ce1834ad298c8e8d270315652bbd6e40cec489f65802db2fdd03167}is .
