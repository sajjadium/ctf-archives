We have several chess matches on an 8x8 board needing to know if either king is in check or not. Below is some starter code that reads some chess board data from several chess matches.

'''
Takes '+' and ' ' delimited data of chess matches and parses into list of seperate matches
''' 
def ParseMatches(chess_matches):
    return [c.split('+') for c in chess_matches.split(' ')]

'''
:param chess_match: A list of chess pieces and their location on the board. ie: ['w,p,a2', 'w,q,a6','w,k,c1','b,r,h1','b,k,g3']
:return: returns True or False if a King is in check
'''
def IsKingInCheck(chess_match):
    # impliment code

# Parses chess matches from raw_input and calls "IsKingInCheck" for each match. Result is then printed
result = []
chess_matches = ParseMatches(raw_input())
for chess_match in chess_matches:
    result.append(IsKingInCheck(chess_match))
    
print result

Impliment "IsKingInCheck" function which takes a single matches' chess data and returns True if the one of the Kings are in check (or checkmate), otherwise False. The single matches' chess data will be a list of pieces and their location on the board in the format of ["color, rank, cordinates"].

Example ["w,p,a2", "w,q,b6", "w,r,h2", "w,k,c1", "w,p,c7", "w,p,g7", "w,p,e6", "b,k,d7", "b,p,e6", "b,r,a6",]

Color

    "b" = Black
    "w" = White

Rank

    "q" = Queen
    "k" = King
    "b" = Bishop
    "r" = Rook
    "n" = Knight
    "p" = Pawn

Cordinates

    This describes where the piece currently is on the board and will be in typical chess cordinates, such as "a6" or "b7", as seen on a labeled chess board.

In this chess game, White opponent starts at the lower numbers of the board cordinates and Black opponent at higher cordinates.

stdin example:

w,p,c6+w,q,c8+w,p,g7+w,k,e5+b,b,b2+b,p,f3+b,k,f1
w,p,c4+w,r,a6+w,p,e6+w,p,h6+w,p,g7+w,k,h5+b,r,b2+b,p,f3+b,k,c2

stdout example:

[True, False]

You can ignore the default code below and instead use code above. Once function is implemented, simply copy/paste into box and run. Ensure not to print anything else during your code execution!
