A cloud of space junk is in your constellation's orbital plane. Use the space lasers on your satellites to vaporize it! Destroy at least 51 pieces of space junk to get the flag.

The lasers have a range of 100 km and must be provided range and attitude to lock onto the space junk. Don't allow any space junk to approach closer than 10 km.

Command format:

[Time_UTC] [Sat_ID] FIRE [Qx] [Qy] [Qz] [Qw] [Range_km]

Command example:

2021177.014500 SAT1 FIRE -0.7993071278793108 0.2569145028089314 0.0 0.5432338847750264 47.85760531563315

This command fires the laser from Sat1 on June 26, 2021 (day 177 of the year) at 01:45:00 UTC and expects the target to be approximately 48 km away. The direction would be a [0,0,1] vector in the J2000 frame rotated by the provided quaternion [-0.7993071278793108 0.2569145028089314 0.0 0.5432338847750264] in the form [Qx Qy Qz Qw].

One successful laser command is provided for you (note: there are many possible combinations of time, attitude, range, and spacecraft to destroy the same piece of space junk):

2021177.002200 SAT1 FIRE -0.6254112512084177 -0.10281341941423379 0.0 0.773492189779751 84.9530354564239
