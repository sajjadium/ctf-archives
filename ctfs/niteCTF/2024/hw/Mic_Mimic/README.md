hardware

You are trying to replicate the Shure ULXD8 X52 wireless mic at a cheaper price to beat the competition. At the final part, as you were measuring and noting down the output characteristics of its ADC, reckless mistakes cause you to short the supply and damage your only copy.

Given the output characteristics of the data, can you figure out what pins you need to set HIGH and LOW in your clone's firmware to get the same output chars(4 pins). You also want to modify the device to accept input only from a signal greater than or equal to 10Hz, what resistor value should you use in your design(round off to the nearest kilo ohm).

Output characteristics:

1)pin 10 and 11 act as outputs

2)A clock signal of around 32khz was supplied to pin 15

3)As soon as you receive the 24th bit from pin 12, pin 10 goes low

a,b,c,d - Mode and format pin numbers in ascending order.

Flag format: nite{a:(1/0),b:(1/0),c:(1/0),d:(1/0),(resistor value in kilo ohm)} - ignore brackets

Author : vikaran
