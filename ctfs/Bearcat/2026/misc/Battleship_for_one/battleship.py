#!/usr/local/bin/python -u
import numpy as np
from time import sleep
from random import randint

class Board:
    def __init__(self, size, attempts, basis=None):
        self.size = size
        self.attempts = attempts
        self.guessed = []
        self.found = False
        self.round_size = self.size * (self.size + 1) // 2
        if basis is None:
            basis = np.arange(size**2)
        self.board = np.array(basis).reshape(size, size)

    def __repr__(self):
        return f'({self.board}, attempts = {self.attempts})'

    def __str__(self):
        print(f'Attempts left: {self.attempts}')
        spacing = int(np.log10(self.size**2-1)) + 1
        if not self.attempts or self.found:
            board_str = '\n'.join([' '.join(map(lambda n: f'{n:0{spacing}}' if n != 0 else f'\033[9{1+self.found}m\033[1m{n:0{spacing}}\033[0m', row)) for row in self.board])
        else:
            masked_board = np.full(self.board.shape, 'X'*spacing)
            for guess in self.guessed:
                masked_board[*guess] = f'{self.board[*guess]:0{spacing}}'
            board_str = '\n'.join(map(' '.join,masked_board))
        return board_str

    def gen_map(self, round_seed):
        indices = list(range(self.size))
        index_map = [0]*self.size
        for i in range(self.size):
            index = round_seed % (self.size - i)
            index_map[i] = indices.pop(index)
            round_seed //= (self.size - i)
        return index_map

    def row_round(self, col_map):
        self.board[col_map] = self.board[range(self.size)]

    def col_round(self, col_map):
        self.board[:, col_map] = self.board[:, range(self.size)]

    def shuffle(self, seed):
        while seed:
            self.row_round(self.gen_map(seed%self.round_size))
            seed //= self.round_size
            self.col_round(self.gen_map(seed%self.round_size))
            seed //= self.round_size
    
    def guess(self, index):
        assert len(index) == 2 \
            and index[0] in range(self.size) \
            and index[1] in range(self.size) \
            and index not in self.guessed
        self.guessed.append(index)
        self.found |= not self.board[*index]
        self.attempts -= 1
        return self.found or not self.attempts
    
def play(board):
    seed = randint(0, 1<<32)
    board.shuffle(seed)
    while True:
        print(board)
        try:
            guess = tuple(map(int,input('Where is the battleship > ').split()))
            if board.guess(guess): break
        except (AssertionError, ValueError):
            print('Enter your guess as "row col"')
    print('Yay you won!' if board.found else 'Try again')
    print(board)
    sleep(0.5)
    print()
    return not board.found

def main():
    easy = (3, 5, (2, 3, 1, 6, 0, 8, 5, 4, 7))
    medium = (10, 20, (25, 32, 97, 0, 18, 10, 3, 61, 85, 43, 46, 28, 13, 51, 16, 50, 83, 6, 98, 91, 14, 20, 87, 86, 99, 42, 55, 27, 64, 22, 26, 96, 70, 24, 38, 1, 62, 63, 7, 29, 84, 89, 59, 88, 11, 49, 76, 17, 31, 12, 65, 41, 21, 95, 68, 19, 80, 90, 36, 45, 39, 78, 34, 67, 69, 57, 23, 52, 15, 30, 48, 92, 56, 72, 40, 9, 54, 35, 74, 53, 37, 71, 4, 94, 73, 79, 77, 75, 81, 47, 60, 44, 33, 8, 82, 2, 58, 66, 93, 5))
    hard = (30, 30, (97, 726, 67, 4, 578, 162, 40, 111, 355, 528, 807, 405, 840, 748, 696, 495, 651, 255, 75, 216, 697, 417, 649, 779, 670, 419, 347, 324, 299, 607, 625, 685, 864, 205, 226, 563, 475, 797, 181, 46, 400, 517, 548, 525, 17, 32, 115, 666, 194, 236, 533, 819, 780, 783, 632, 661, 77, 196, 826, 523, 204, 338, 310, 210, 654, 86, 627, 453, 39, 689, 634, 284, 615, 1, 293, 199, 375, 78, 772, 93, 348, 117, 862, 825, 529, 129, 526, 159, 881, 623, 401, 161, 339, 6, 682, 251, 622, 577, 378, 14, 688, 137, 441, 383, 275, 354, 641, 291, 88, 793, 136, 411, 222, 466, 82, 412, 767, 721, 267, 359, 274, 188, 898, 574, 695, 31, 169, 488, 277, 630, 485, 197, 332, 72, 809, 265, 92, 705, 479, 818, 478, 257, 158, 189, 813, 126, 157, 888, 518, 455, 770, 297, 176, 302, 717, 690, 91, 203, 276, 564, 652, 171, 100, 131, 56, 683, 633, 853, 710, 507, 36, 114, 508, 259, 560, 647, 150, 246, 104, 130, 337, 427, 191, 358, 66, 48, 565, 83, 123, 566, 535, 305, 681, 116, 45, 27, 899, 811, 784, 228, 28, 482, 49, 367, 592, 285, 606, 418, 263, 795, 693, 395, 814, 877, 530, 861, 759, 663, 406, 514, 394, 451, 119, 264, 52, 109, 712, 183, 110, 890, 701, 676, 872, 588, 147, 73, 830, 415, 142, 587, 99, 559, 459, 335, 87, 201, 174, 846, 261, 152, 894, 313, 727, 320, 646, 552, 319, 706, 740, 489, 245, 791, 132, 687, 571, 513, 889, 164, 398, 747, 21, 599, 12, 510, 842, 631, 329, 773, 755, 538, 613, 154, 580, 590, 591, 5, 209, 735, 330, 838, 180, 386, 742, 200, 388, 610, 311, 597, 762, 294, 215, 448, 512, 817, 340, 884, 576, 202, 351, 743, 0, 118, 242, 640, 794, 212, 430, 403, 700, 655, 473, 644, 103, 503, 545, 886, 680, 172, 757, 231, 64, 602, 439, 758, 760, 867, 833, 273, 177, 876, 679, 896, 594, 550, 626, 334, 511, 360, 600, 182, 452, 399, 42, 667, 527, 279, 193, 155, 737, 754, 318, 589, 851, 13, 822, 751, 570, 669, 328, 391, 151, 234, 153, 583, 650, 300, 19, 143, 184, 604, 361, 312, 120, 873, 409, 206, 848, 29, 168, 628, 875, 829, 465, 57, 303, 94, 531, 134, 288, 389, 897, 858, 278, 266, 498, 522, 802, 433, 855, 831, 716, 792, 771, 230, 657, 540, 752, 18, 471, 65, 3, 470, 573, 584, 568, 44, 639, 390, 553, 232, 586, 892, 782, 425, 775, 834, 859, 749, 316, 603, 96, 443, 167, 323, 106, 2, 170, 282, 786, 326, 380, 691, 887, 637, 436, 420, 536, 208, 69, 460, 352, 800, 857, 186, 445, 429, 739, 144, 520, 609, 593, 41, 785, 738, 50, 532, 424, 828, 581, 397, 504, 608, 768, 250, 745, 227, 468, 844, 778, 801, 221, 356, 719, 135, 789, 253, 22, 790, 384, 612, 761, 125, 423, 672, 744, 89, 704, 803, 871, 648, 229, 108, 621, 325, 146, 557, 467, 729, 422, 327, 128, 10, 662, 617, 885, 237, 372, 307, 145, 796, 866, 233, 301, 447, 20, 763, 653, 414, 107, 296, 163, 173, 365, 58, 668, 98, 750, 438, 476, 344, 713, 718, 708, 549, 816, 671, 74, 539, 252, 160, 224, 658, 781, 642, 54, 35, 869, 321, 434, 839, 665, 101, 854, 746, 223, 404, 605, 562, 492, 258, 481, 707, 483, 852, 149, 95, 774, 636, 674, 113, 806, 55, 382, 551, 247, 413, 863, 33, 156, 407, 43, 561, 724, 286, 148, 856, 190, 702, 298, 731, 239, 220, 217, 457, 698, 870, 506, 244, 30, 678, 353, 368, 271, 841, 741, 891, 893, 8, 444, 381, 753, 595, 357, 336, 124, 616, 804, 207, 815, 798, 805, 554, 408, 416, 656, 322, 827, 213, 225, 837, 736, 824, 734, 694, 575, 516, 280, 619, 703, 544, 611, 127, 505, 343, 84, 664, 477, 270, 845, 723, 449, 63, 832, 618, 331, 843, 370, 660, 256, 369, 366, 81, 385, 102, 80, 486, 421, 428, 521, 26, 214, 490, 175, 25, 596, 868, 555, 195, 426, 112, 725, 582, 883, 140, 874, 437, 34, 558, 306, 166, 524, 341, 474, 262, 765, 493, 314, 165, 614, 711, 105, 260, 469, 720, 501, 699, 11, 317, 541, 860, 138, 37, 315, 272, 677, 585, 121, 454, 374, 432, 462, 730, 865, 393, 133, 450, 308, 464, 499, 624, 51, 350, 882, 497, 733, 248, 387, 392, 254, 638, 431, 756, 812, 776, 410, 192, 287, 179, 645, 643, 543, 7, 59, 268, 880, 362, 515, 240, 38, 47, 820, 249, 185, 456, 346, 823, 243, 281, 673, 122, 68, 849, 290, 766, 295, 487, 463, 23, 635, 547, 269, 24, 376, 349, 70, 211, 732, 810, 141, 787, 440, 219, 684, 396, 16, 821, 534, 218, 542, 373, 292, 500, 519, 62, 878, 435, 484, 895, 675, 709, 799, 808, 659, 458, 304, 85, 402, 620, 835, 289, 502, 342, 569, 598, 309, 9, 714, 53, 364, 446, 377, 60, 178, 722, 686, 235, 71, 556, 333, 187, 90, 494, 496, 777, 567, 579, 363, 139, 764, 601, 379, 692, 879, 61, 509, 345, 715, 491, 537, 283, 442, 15, 546, 472, 836, 76, 198, 480, 79, 371, 769, 788, 572, 241, 728, 238, 847, 461, 629, 850))
    print('Welcome to solo battleship!')
    while True:
        print('Choose your difficulty:')
        print('\t1. Easy')
        print('\t2. Medium')
        print('\t3. Hard')
        print('\t4. Ultimate Challenge')
        print('\t5. Exit')
        choice = input()
        match choice:
            case '1':
                play(Board(*easy))
            case '2':
                play(Board(*medium))
            case '3':
                play(Board(*hard))
            case '4':
                for _ in range(10):
                    if play(Board(*easy)): break
                else:
                    for _ in range(10):
                        if play(Board(*medium)): break
                    else:
                        for _ in range(10):
                            if play(Board(*hard)): break
                        else:
                            print('You are truly the greatest admiral we have seen')
                            print(open('flag.txt').read())
                            return
                print("Sorry skipper, looks like you just arn't up to it.")
            case '5':
                print('Thank you for playing!')
                break
            case _:
                print('There was an error with your input. Please try again.')
            
if __name__ == '__main__':
    main()