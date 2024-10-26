very easy

Here is a database of sells on a online marketplace. Your job as a data analyst is to answer the following questions :
1. If at 2019-12-31 (at the beginning) every person has 10000$, who has the most money by 2023-01-01 (transaction of that day excluded)?
2. By 2023-01-01 (transaction of that day excluded) how much money was spared through discounts?
3. By 2023-01-01 (transaction of that day excluded) how many people have a negative balance?

Here are some information about the database fields:
 Field name | Data type | Constraints 
------------|------------|-------------------------
 order_id | integer | 1 < order_id < 100 000 
 buyer_id | integer | 1 < buyer_id < 100 000 
 seller_id | integer | 1 < seller_id < 100 000 
 price | integer | 1 < price < 10 000 
 discount | integer | 0 < discount < 100 
 date | date | yyyy-mm-dd 

Additionally, you should know that Buyers and Sellers are reprensted by a unique ID and are correlated. Buyer 163564 is the same person as Seller 163564.

Prices should be floored to the nearest integer, but only at the final stage of the calculation.

e.g. If there are two discounts bringing prices down from 10 and 5 to 8.64 and 4.32 respectively, the amount of money spared is 10 + 5 - 8.64 - 4.32 = 2.04 ~= 2. As you can see, the only rounding operation was done on the very last value, used in the flag.

The flag is Hero{response1_response2_reponse3}.

e.g. Hero{163564_21673_78}

Format : Hero{flag}
Author : Log_s
