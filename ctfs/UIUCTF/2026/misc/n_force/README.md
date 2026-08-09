hard
In 1796, Carl Friedrich Gauss famously proved that the 17-gon was constructible by compass and straightedge. In 1894, Johann Gustav Hermes spent 10 years detailing the compass-and-straightedge construction of the 65537-gon.

However, the minimum number of steps for these constructions remains unknown - until today maybe? Submit your constructions at https://n-force.2026.uiuc.tf/ to fight for a spot on the leaderboard - below is an example of a .geo file describing the construction of an equilateral triangle:

# Comments are suppported via hashtags
# We start with two points, O = (0,0) and P = (1, 0)
circle O P C1 # construct a circle centered at O with point P on the circle called C1
circle P O C2 # construct a circle centered at P with point O on the circle called C2
meets_circle_circle C1 C2 A B # construct two points where C1 and C2 meet and label them as A and B
n_gon P B O # assert that points P, B, and O form a regular 3-gon
Other commands are available - attached is the parser which you can use to verify your constructions locally.

Each of the five construction categories awards up to 200 CTF points. Points use logarithmic placement within that category: first place receives 200, the bottom score group receives 50, and tied scores receive equal points.

author: epistemologist
