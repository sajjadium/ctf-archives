from random import shuffle
from random import randint 

FLAG = open("./flag", "rb").read()

flagbanner = f'''
|| 
||   .,,;;;;;;,,.. 
||.;;;;;;*;;;;;;;*;;, ..,,;;;;;;%%%%%, 
||';*;;;;;;;;*;;;;;;,::*::;;;*;;%%%%%%>>%%%%%,                 .; 
|| ';;;;;*;;;;;;;;*;;,:::::*;;;;;@@@##>>%%%%%%,        ..,,;%%%%' 
||  ;*;;;;;;;;*;;;;;;,::*;:;;;;*;@@@@##ooO0@@##>>%%%%%%%%%%%%%%' 
||  ;;;;;;*;;;;;;;;*;;,:;:::*;;;;%%%%%%ooO0@@##>>%%%%%%%%%%a@@' 
||  ;;*;;;;;;;;;*;;;;;,::*;::;;;*;%%%%%%>>%%%%%%ooO@@@@@@@@@@@ 
||  ;;;;;;*;;;;;;;;*;;,:::::;*;;;;@@@@##>>%%%%%%%ooO@@@@@@@@%% 
||  ;;*;;;;;;;;;*;;;;;;,::*;:;;;*;@@@@@##ooO0@@##>>%%%%%%%%%%% 
||  ;;;;;;;*;;;;;;;*;;;,:::::*;;;;;%%%%%%ooO0@@@##>>%%%%%%%%a@, 
||  ;;;*;;;;;;;;*;;;;;;,::*:;;;;;*;%%%%%%%>>%%%%%%%%ooO@@@@@@@@ 
||  ;;;;;;;*;;;;;;;;*;;;,::::;*;;;;@@@@@##>>%%%%%%%%%ooO@@@@@%%' 
||  ;;*;;;;;;;;*;;;;;;;;,::*:;;;:;*;@@@@@##ooO0@@@@##>>%%%%%%%% 
||  ;;;;;;;*;;;;;;*;;;;*;,::::;*;;;;;%%%%%%ooO00@@@@##>>%%%%%a@ 
||  ;*;;a@@@#######@@@@@a,:::*;;;;;;*;%%%%%%>>%%%%%%%%%ooO@@@@@, 
||  ;;@@@@@@#######@@@@@##ooO00@@@@@@@@@@@##>>%%%%%%%%%%ooO@@@%% 
||  a@@@%%%%%%%%%%%%%%%%%%ooO00@@@@@@@@@@@@##ooO0@@@@##>>%%%%%%% 
||  @@%%%%%%%%%%%%%%%%%%%%%>>%%%%%%%%%%%%%%%%ooO00@@@@##>>%%%a@@ 
||  %%%%a@@##########@@@@##>>%%%%%%%%%%%%%%%%%>>%%%%%%%%%ooO@@@a 
||  %%@@@@@##########@@@@@##ooO0@@@@@@@@@@@@##>>%%%%%%%%%%ooO@%% 
||  a@@@%%%%%%%%%%%%%%%%%%%%ooO0@@@@@@@@@@@@@##ooO0@@@@##>>%%%%%. 
||  @@%%%%%%%%%%%%%%%%%%%%%%%>>%%%%%%%%%%%%%%%%ooO0@@@@@##>>%%%a@ 
||  %%%%a@@############@@@@##>>%%%%%%%%%%%%%%%%%>>%%%%%%%%%%ooO@@a 
||  %%@@@@@############@@@@@##ooO0@@@@@@@@@@@@##>>%%%%%%%%%%%ooO%% 
||  a@@@%%%%%%%%%%%%%%%%%%%%%%ooO0@@@@@@@@@@@@@##ooO0@@@@##%>>%%%% 
||  @@%%%%%%%%%%%%%%%%%%%%%%%%%>>%%%%%%%%%%%%%%%%ooO0@@@@@##>>%%a@ 
|| .%%%'                        `>%%%%%%%%%%%%%%%%>>%%%%%%%%%ooO@@, 
||.%%                                             `>%%%%%%%%%ooO%%% 
||'                                                          `%%%%% 
||                                                            `%%' 
|| 
|| 
|| 
|| 
|| 
|| 
|| 
|| 
|| 
|| 
|| 
--
'''

truth = lambda r : not not r 
lie = lambda r : not r 


_filter = ["1", "0", " ", "==", "!=", "or", "and", "not", "(", ")"]

def expr_val(expr, ident, answer):
    sheep = ident[:]
    return answer(eval(expr))

def failed():
    print("You failed, sheep ~~commander~~")
    exit(0)

from secrets import generate_trust_network 
def intro():
    print("Another day begin at The Sheep Village! You ( commander of the sheep) wake up as usually and start patroling around...")
    print("Suddenly you hear a loud scream coming from inside village. You immediately rush to the crowd.")
    print("'This cant be real...' - You come close and realize that there are 2 dead body (sheeps, of course) lying on the ground")
    print("You found that there are signs of wolves responsible for those deaths ")
    print("The peace has been broken again. Dear commannder, you have to find them before they onslaught all of us!")

def challenge_for_stage1():
    N = 50 # I can set N to random, but it will cost more time to solve
    wolf_num = randint(1, 3) * 2
    trust, wolves = generate_trust_network(N, wolf_num)
    for idx, trust in enumerate(trust):
        print(f"The (sheep) {idx} trust: {trust}")
    

    print("Who is guilty?")



    ans = eval(input())
    assert(all((ans.count(i) == 1) and (i >=0 and i < N) for i in ans))
    assert(all((wolves.count(i) == 1) and (i >=0 and i<N) for i in wolves))
    ans.sort()
    wolves.sort()

    if ans == wolves:
        print("CORRECT!")
        return True 
    else:
        print("WRONG!")
        return False
    pass

def stage1():
    # In order to simplify the stage (so you have time to do other challenge), I decide to guide you how to solve it

    # The challenge is simple: there are N sheep with 2 wolves (there is no clues to distinguish them with other sheep)
    # But there is one clue - trust, each sheep (or wolf) trust some of their friend (which can be also a wolf), for now
    # I will refer it as connection . 
    # For simplify, lets the sheep (wolf) note as a node, the trust between them as an edge( undirected edge, trust are based on both side)
    # if 1 connect 2, 2 connect 3, then 1 also connect 3
    # as the sheep village are a strongly unite, also are their trust.
    # for example: 1 connect 2, 2 connect 3, 3 connect 1
    # if 1 decide not to trust 2 (erase edge 1 2), then 1 still trust 2 as 1 - 3, 3 - 2
    # Right now, 2 wolves sneak in, working together, creating trust between other sheeps (there is an edge between them)
    # The key to find them is, if they are isolate (there is no connect between them, or the edge between them is deleted), 
    # then the graph is not strong unite anymore
    # which mean, there is A and B who does not trust each other (or there is no connection between A and B if the edge is deleted)
    # (the graph will be assured that number of wolf is even, and there is exactly 1 connection for each wolf)
    # for example, in the graph:     2        6
    #                               | \     / |
    #                               |  1---4  |
    #                               | /     \ |
    #                                3       5
    # 1 and 4 will be the wolves (the graph will ensure there is exactly 1 edge each wolf, no wolf work alone)
    # thats all what I want to tell about this stage. Good luck
    print("STAGE 1")

    for i in range(50):
        print(f"ROUND {i}")
        if not challenge_for_stage1():
            return False
        
    return True
    

def challenge_for_stage2(N, q, maxlies):
    print(f"This time, there are {N} sheep (including wolves, those disguise and hide in the crowd, so you have no clue to distinguish them with the rest). ")
    print("The crowd become chaos when they know among them, there are wolves waiting them to be their lunch.")
    print("Luckily, a sage sheep appear and agree to help you. He will answer your questions, only Yes or No")
    print("But becareful, sage sheep can lie at most 2 times (as you refuse to pay him overtime)")

    
    lie_times = randint(0, maxlies)
    identity = [randint(0, 1) for i in range(N)]
    answer = [truth] * (q - lie_times) + [lie] * lie_times
    shuffle(answer)
    filterlist = _filter + [f"sheep[{i}]" for i in range(N)]

    #DEBUGGING Section, remember to delete it after  finish testing
    # print(identity)
    #END of DEBUGGING Section

    for idx  in range(q):
        print(f"What would you want to ask in the {idx}-th question:")
        question = input()
        for i in question.split():
            try:
                assert i in filterlist
            except:
                print("Wrong question, commander!")
                exit(0)
        
        if expr_val(question, identity, answer[idx]):
            print("Yes")
        else:
            print("No")
    print("What is your final decision? Who are them?")
    final_ans = [int(i) for i in input().split()]
    if final_ans == identity:
        print("CORRECT")
        return True     
    else:
        print("WRONG")
        return False 


def stage2():
    print("STAGE 2")
    for i in range(50):
        print(f"ROUND {i}")
        if not challenge_for_stage2(5, 11, 1):
            return False
    print("Suddenly, sage sheep want to test your skill, and he decide to trick you at most twice.")
    for i in range(50):
        print(f"ROUND {i + 20}")
        if not challenge_for_stage2(7, 15, 2):
            return False
    return True 

def stage3():

    return True
    # out of idea to make stage 3 :))))


def challenge():
    intro()
    if not stage1():
        failed()

    if not stage2():
        failed()

    if not stage3():
        failed()

    print("Commander, we have successfully stopped those evil wolves!!!")
    print(flagbanner)
    print(f"THE VICTORY FLAG IS RISING : {FLAG}.")



challenge()