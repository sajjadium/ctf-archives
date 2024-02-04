# Dr. Dai and His Pals

## Problem Description
Dr. Dai raises many Pals for his scientific research. As Dr. Dai is a loving person, he prepares food for these Pals every day.

Now we have $x$ Pals that only love to eat meat, $y$ Pals that absolutely do not eat meat, and $c$ Pals that eat anything.

The East-1th student canteen provides $m$ types of dishes and stipulates that each dish can only be bought once. The $i$-th dish has a price $c_i$, and has a character $A$ or $B$, indicating whether it is a meat dish or a vegetarian dish.

Now, Dr. Dai hopes to feed as many Pals as possible and, given the limited research funds, also hopes to minimize the cost under this premise. Please calculate the maximum number of Pals he can feed, and the minimum amount of money he needs to spend in this situation.

## Input Format
The first line contains three integers $a$ $b$ $c$

The next line is an integer $m$

The following $m$ lines, each representing the value and category of the food, A for vegetarian, B for meat.

## Output Format
Two numbers, representing the number of Pals that can be fed and the total cost, respectively.

## Sample #1
### Sample Input #1
2 1 1
4
5 A
6 B
3 B
7 B
### Sample Output #1
3 14

## Tips
For 10% of the data, it is guaranteed that $a=b=0$

For 30% of the data, it is guaranteed that $1 \leq a,b,c \leq 100, 1 \leq m \leq 100$

For 100% of the data, it is guaranteed that $1 \leq a,b,c \leq 10^5, 1 \leq m \leq 3 \times 10^5$

All $c_i \leq 10^9$