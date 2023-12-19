from stockfish import Stockfish
stockfish = Stockfish(path='/usr/bin/stockfish/stockfish-ubuntu-x86-64-avx2')

{
    "Debug Log File": "",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": 4,
    "Ponder": "false",
    "Hash": 2048,
    "MultiPV": 1,
    "Skill Level": 69,
    "Move Overhead": 10,
    "Minimum Thinking Time": 60,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 3600
}

blacklist = [ "import", "open",  "module", "write", "load", "read", "flag", "eval", "exec", "system", "os", "_", "#", "'", "\"" ]

print("_______________________________________")
print("|                                     |")
print("|       WELCOME TO UNFAIR CHESS!      |")
print("|                                     |")
print("|    You know the rules and so do I!  |")
print("|_____________________________________|")
print()
stockfish.set_fen_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(stockfish.get_board_visual())
count = 0
all_moves = list()

try:
    while count<150:
        user_move = ""
        while user_move == "":
            user_move = input("Your move: ").strip()
            if user_move:
                all_moves.append(user_move)
                stockfish.make_moves_from_current_position([user_move])
                print(stockfish.get_board_visual())
            else:
                print("Error: Empty input. Please enter a valid move.")


        stockfish.make_moves_from_current_position([stockfish.get_best_move()])
        print(stockfish.get_board_visual())
        count += 1

        change = stockfish.get_fen_position().split()
        change[1] = 'b'
        changed = ' '.join(change)
        stockfish.set_fen_position(changed)

        stockfish.make_moves_from_current_position([stockfish.get_best_move()])
        print(stockfish.get_board_visual())
        count += 1
        
        print(count)

except:
    if(count>50):
        print("Wow, you are incredible! Now, lets check your execution in this game.")
        result = "".join(all_moves)

        if not any(any(word in result for word in blacklist_word.split()) for blacklist_word in blacklist):
            exec(result)
        else:
            print("Invalid characters.")
    else:
        print("GAME OVER!")

        
