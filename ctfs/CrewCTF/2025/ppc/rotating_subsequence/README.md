Do you like weird challenges? Me too!

author: KLPP


Let's pick a number K.

When we have a sequence $A=a_1,a_2,\dots,a_x$, we can say that a non-empty subsequence (not necessarily contiguous) of the elements of $A$, identified by indices $b_1,b_2,\dots,b_y$ is rotating if $a_{b_{i+1}}=a_{b_i}+1 (mod K)$ for all $i$ in $1,2,\dots,y-1$, and also $b_i < b_{i+1}$ (the indices always go from left to the right).

Also, notice that $y$ can be equal to 1.

Notice that the indices matter.

Given $N,K$ your job is to create a sequence $S$ such that $S$ has exactly $N$ rotating subsequences.

Also, don't make the sequence too big!

Example: If $K=2$ and $A=\[0,1,0,1\]$, then the first and second element form a rotating subsequence, but the first and third do not, as $0 \neq 0+1 (mod 2)$.
In this sequence for example there are exactly 11 rotating subsequences, with indices (0 indexed):

0

1

2

3

0,1

1,2

2,3

0,3

0,1,2

1,2,3

0,1,2,3

Notice, for example, if K=3, then there would be 7 rotating subsequences.

0

1

2

3

0,1

2,3

0,3

Also notice that despite [0] and [2] being "equal" subsequences they are counted separately because we are counting by the indexes.
