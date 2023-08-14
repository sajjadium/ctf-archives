from math import sqrt

# country capital coordinates
capital = (832, 500)

# town coordinates
towns = [(523, 832), (676, 218), (731, 739), (803, 858),
 (170, 542), (273, 743), (794, 345), (825, 569), (770, 306),
 (168, 476), (198, 361), (798, 352), (604, 958), (700, 235),
 (791, 661), (37, 424), (393, 815), (250, 719), (400, 183),
 (468, 831), (604, 184), (168, 521), (691, 71), (304, 232),
 (800, 642), (708, 241), (683, 223), (726, 257), (279, 252),
 (559, 827), (832, 494), (584, 178), (254, 277), (309, 772),
 (293, 240), (58, 658), (765, 300), (446, 828), (766, 699),
 (407, 819), (818, 405), (626, 192), (828, 449), (758, 291),
 (333, 788), (124, 219), (443, 172), (640, 801), (171, 452),
 (242, 710), (496, 168), (217, 674), (785, 672), (369, 195),
 (486, 168), (821, 416), (206, 654), (503, 832), (288, 756),
 (789, 336), (170, 464), (636, 197), (168, 496), (832, 515),
 (168, 509), (832, 523), (677, 781), (651, 796), (575, 176),
 (478, 168), (831, 469), (391, 186), (735, 265), (529, 169),
 (241, 292), (235, 700), (220, 321), (832, 481), (806, 629),
 (176, 575), (751, 282), (511, 832), (581, 822), (708, 759),
 (777, 317), (410, 180), (180, 411), (382, 189), (694, 230),
 (327, 784), (177, 421), (797, 650), (742, 272), (719, 250),
 (739, 731), (298, 764), (423, 177), (658, 792), (813, 611),
 (667, 213), (257, 727), (178, 583), (616, 189), (342, 208),
 (817, 600), (348, 205), (344, 793), (968, 541), (700, 766),
 (181, 594), (633, 804), (656, 206), (831, 533), (722, 747),
 (759, 708), (188, 615), (416, 822), (820, 590), (169, 529),
 (172, 445), (424, 824), (687, 775), (229, 692), (597, 182),
 (187, 388), (436, 826), (463, 170), (321, 220), (174, 434),
 (567, 826), (224, 686), (210, 338), (608, 814), (190, 381),
 (538, 170), (332, 938), (265, 735), (195, 367), (173, 562),
 (270, 260), (462, 830), (192, 625), (824, 427), (781, 678),
 (599, 817), (669, 786), (359, 199), (328, 216), (183, 401),
 (815, 393), (827, 559), (830, 460), (215, 329), (311, 227),
 (713, 755), (822, 581), (546, 829), (505, 168), (172, 554),
 (748, 721), (421, 37), (184, 604), (317, 778), (286, 246),
 (648, 202), (201, 645), (281, 750), (453, 171), (356, 800),
 (827, 439), (491, 832), (375, 808), (807, 372), (521, 168),
 (246, 286), (482, 832), (804, 365), (809, 622), (197, 637),
 (232, 303), (227, 310), (362, 802), (592, 819), (533, 831),
 (560, 173), (550, 171), (619, 810), (384, 811), (931, 313),
 (811, 384), (168, 488), (773, 690), (781, 323), (204, 349),
 (213, 667), (829, 547), (431, 175), (754, 714), (263, 267)]

def calcDistance(start,finish):
    dist = sqrt((start[0]-finish[0])*(start[0]-finish[0]) +
                (start[1]-finish[1])*(start[1]-finish[1]))
    return dist

# calculates the distance along a path consisting of a list of town coordinates
def calcPath(path):
    pathLen = 0
    for i in range(1,len(path)):
        pathLen+=calcDistance(path[i],path[i-1])
    return pathLen

def getFlag(permutation):
    enc = b"]V\xa8\x1ef\x91\x02\xde\x1f\x9a\xd1\x8ck_\xdb\x15\xd5\xe3\xb0\xef\xb8\x1e \xa91L\x8d#Q\xd7\xf3\xf5\x9d6\x8f>q2\xf9\xc3R\xda\x11_m\xff\\\xfc\x93\x19c\xf1r\xb1\x80\xde'\xfepk;\xc23\x87\x13\xdf3\xffZtF6\x7f\x88w\xd7\xa9\xd1\xfa,\xf6\xa82\xe1\x01\x1aS\xae\xcf\xb48\xa6\x97|$\xaa\xa9\x05\x86\xa8b\xe6\xbb\xb4\xfc\xd1(WZ,Beg\xe19\x1d\x9a\xa4u\xf2[:4'\xef5\trg\x0eV\x97X\x80\x92\xe0\t\xfd\xa0\x9e\xc6\xa3g\x12\xe9\xfb\x1f\x8a\x05\x116\xdc\x9eI\x9bY\xf9z\x01X\x80U{\x98\xf2@r\t\x9cz\xd8\xcb\x03\xe1\x99\x93\xec\xa7\xdf#\x86\xc90\x90\xc5\xca\xd8\xfa\xd1d\xbbq~ \xce\xa9\xefh\xd5"
    data = [enc[i] for i in permutation]
    flag = [0]*60
    for i in range(len(data)):
        flag[i%60]=flag[i%60]^data[i]
    return bytes(flag)

if __name__ == "__main__":
    print(f"We have a capital and {len(towns)} towns in our fantasy country.")
    print("We need to develop shortest path for our owl to visit all towns starting from capital.")
    print("Town coordinates listed below:\n")
    coordinates = ""
    for i in range(len(towns)):
        coordinates+=str(towns[i])+'\t'
        if i % 5 == 4:
            coordinates+='\n'
    print(coordinates)
    print(f"If we send an owl to visit the cities in this order, it will fly a total of {calcPath([capital]+towns)} kilometers.")
    print("We believe that the best path exist.")
    user_input = input("Please enter best permutation of this towns list.\n*just numbers, space-separated for example: 0 1 2 3 4 ... 198\n")
    permutation = tuple(int(item) for item in user_input.split())
    if set(permutation) != set(range(199)):
        print("invalid permutation")
    else:
        best_path = [capital] + [towns[i] for i in permutation]
        print(f"You path takes a total of {calcPath(best_path)} kilometers.")
        print(f"If you're sure it's the best permutation, then here's your flag:\n{getFlag(permutation)}")
    
    
    
        
