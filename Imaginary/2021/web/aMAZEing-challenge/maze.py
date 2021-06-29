import random
from os import system
from time import sleep
from solver import solve


START_POS = (1, 1)
MIN_STEPS = 2

WALL = "▓▓"
NEWLINE = "\n"
CLEAR = "  "
FLAG = "{}"
PLAYER = "[]"

WALL_ALT = "##"
NEWLINE_ALT = "n"

UP, LEFT, DOWN, RIGHT = "w", "a", "s", "d"


class Maze:
    def __init__(self, size=(79,39), data=None, verbose=False):
        self._player_pos = START_POS
        self._flag_at = (-1, -1)
        self._maze = [[Node(-1, -1)]]

        if data is None:
            min_steps = (size[0] + size[1]) // 3 * 2 # make sure the flag is far from the start pos
            self.gen_maze(size, min_steps, verbose)
        else:
            self.parse_maze(data)

    def gen_maze(self, size, min_steps, verbose):

        # init all nodes as walls
        self._maze = []
        for i in range(size[1]):
            line = []
            for j in range(size[0]):
                line.append(Node((i, j)))
            self._maze.append(line)

        def calc_new_frontier_cells(pos, passage, frontier):
            i, j = pos

            # add new frontiers for given pos
            if i > 2 and (i - 2, j) not in passage and (i - 2, j) not in frontier:
                frontier.append((i - 2, j))

            if j > 2 and (i, j - 2) not in passage and (i, j - 2) not in frontier:
                frontier.append((i, j - 2))

            if i < size[1] - 3 and (i + 2, j) not in passage and (i + 2, j) not in frontier:
                frontier.append((i + 2, j))

            if j < size[0] - 3 and (i, j + 2) not in passage and (i, j + 2) not in frontier:
                frontier.append((i, j + 2))

        def get_between_cell(pos, passage):
            valid_neighbours = []
            i, j = pos

            for c in passage:
                if c in [(i - 2, j), (i, j - 2), (i + 2, j), (i, j + 2)]:  # cell is a neighbour of pos
                    valid_neighbours.append(c)

            if len(valid_neighbours) == 0:
                return valid_neighbours

            ni, nj = random.choice(valid_neighbours)
            between_cell = ((i + ni) // 2, (j + nj) // 2)  # avg of coords== between cell coords
            return between_cell

        def get_node_from_pos(pos):
            return self._maze[pos[0]][pos[1]]

        # init start pos as passage
        start_cell = get_node_from_pos(START_POS)
        start_cell.clear_wall()

        # init frontier algo, add start_pos to passage and frontier = []
        passage = [START_POS]
        frontier = []
        calc_new_frontier_cells(START_POS, passage, frontier)

        # create the maze with the prim's algorithm
        while len(frontier) > 0:
            if verbose:
                # Just overwrite all previous data with this big a** string
                system("clear")
                print(self.__str__())
                sleep(0.01)

            # choose a random frontier cell
            cell_pos = random.choice(frontier)
            between_cell_pos = get_between_cell(cell_pos, passage)
            frontier.remove(cell_pos)

            cell = get_node_from_pos(cell_pos)
            cell.clear_wall()
            between_cell = get_node_from_pos(between_cell_pos)
            between_cell.clear_wall()

            # between cells are not valid next cells, only the cell variables!
            passage.append(cell_pos)

            # now add the new frontier cells
            calc_new_frontier_cells(cell_pos, passage, frontier)

        # assert that flag pos is far away from player, throws error if no path found from flag to player
        while True:
            self._flag_at = random.choice(passage)
            way = solve(self)

            if verbose:
                system("clear")
                print(self.__str__())
                sleep(0.5)

            if len(way) >= min_steps:
                # maze generated and flag is far enough from the player -> done

                if verbose:
                    print("There is no such thing as an polynomial runtime algorihtm for finding the shortest path between two points. Or is there?")
                    print("CiMgc2VhcmNoIGNsb3Nlc3QgcGF0aCB0byBmbGFnCmRlZiBzb2x2ZShtYXplKToKICAgICMgcmVzZXQgYWxsZSBub2RlIGRpc3RhbmNlcyBhbmQgcHJldiBub2RlcwogICAgbWF6ZS5yZXNldF9zb2x2ZSgpCgogICAgIyBpbml0CiAgICBzdGFydF9ub2RlID0gbWF6ZS5nZXRfcGxheWVyX25vZGUoKQogICAgc3RhcnRfbm9kZS5zZXRfZGlzdCgwKQogICAgdGFyZ2V0ID0gbWF6ZS5nZXRfZmxhZ19ub2RlKCkKCiAgICB2aXNpdGVkID0gW10KICAgIG5leHRfbm9kZXMgPSBbc3RhcnRfbm9kZV0KCiAgICB3aGlsZSB0YXJnZXQgbm90IGluIHZpc2l0ZWQ6CiAgICAgICAgIyBjdXJyZW50IG5vZGUgaXMgYWx3YXlzIHRoZSBvbmUgd2l0aCB0aGUgc2hvcnRlc3QgZGlzdCB0byBzdGFydAogICAgICAgIGN1cnJlbnRfbm9kZSA9IG5leHRfbm9kZXMucG9wKDApCgogICAgICAgIG5laWdoYm91cnMgPSBtYXplLmdldF9hY3Rpb25zKG9ubHlfZGlyZWN0aW9ucz1GYWxzZSwgcG9zPWN1cnJlbnRfbm9kZS5nZXRfcG9zKCkpCiAgICAgICAgZm9yIGRpcmVjdGlvbiwgbmVpZ2hib3VyIGluIG5laWdoYm91cnM6CgogICAgICAgICAgICAjIGNoZWNrIGlmIHRoZSBuZXcgd2F5IGlzIHNob3J0ZXIKICAgICAgICAgICAgbmV3X2Rpc3QgPSBjdXJyZW50X25vZGUuZ2V0X2Rpc3QoKSArIDEKCiAgICAgICAgICAgIGlmIG5ld19kaXN0IDwgbmVpZ2hib3VyLmdldF9kaXN0KCk6CiAgICAgICAgICAgICAgICBuZWlnaGJvdXIuc2V0X2Rpc3QobmV3X2Rpc3QpCiAgICAgICAgICAgICAgICBuZWlnaGJvdXIuc2V0X3ByZXYoZGlyZWN0aW9uLCBjdXJyZW50X25vZGUpCiAgICAgICAgICAgICAgICBuZXh0X25vZGVzLmFwcGVuZChuZWlnaGJvdXIpCgogICAgICAgIGlmIGN1cnJlbnRfbm9kZSA9PSB0YXJnZXQ6CiAgICAgICAgICAgIHByaW50KCkKCiAgICAgICAgdmlzaXRlZC5hcHBlbmQoY3VycmVudF9ub2RlKSAgIyBub3cgYWxsIG5laWdoYm91cnMgYXJlIHZpc2l0ZWQsIG5vIG1vcmUgY2hhbmdlcyB0byBjdXJyZW50IG5vZGUKICAgICAgICBuZXh0X25vZGVzID0gc29ydGVkKG5leHRfbm9kZXMsIGtleT1sYW1iZGEgbjogbi5nZXRfZGlzdCgpKQoKICAgICMgYmFja3RyYWNrIGRpcmVjdGlvbnMKICAgIHdheSA9ICIiCiAgICBub2RlID0gbWF6ZS5nZXRfZmxhZ19ub2RlKCkKICAgIHdoaWxlIG5vZGUgaXMgbm90IHN0YXJ0X25vZGU6CiAgICAgICAgZCwgbm9kZSA9IG5vZGUuZ2V0X3ByZXYoKQogICAgICAgIHdheSArPSBkCgogICAgcmV0dXJuIHdheVs6Oi0xXQoKCmlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICBmcm9tIG1hemUgaW1wb3J0IE1hemUKCiAgICBtID0gTWF6ZSh2ZXJib3NlPUZhbHNlKQogICAgZGlyZWN0aW9ucyA9IHNvbHZlKG0pCgogICAgbS5zaG93X3NvbHZlKGRpcmVjdGlvbnMpCiAgICBwcmludChkaXJlY3Rpb25zKQ==")
                break

    def parse_maze(self, string):
        if NEWLINE in string:
            raw_maze = string.split(NEWLINE)[:-1]
        else:
            raw_maze = string.split(NEWLINE_ALT)[:-1]

        self._maze = []

        for i in range(len(raw_maze)):
            line = []

            for j in range(0, len(raw_maze[i]), 2):  # maze chars are 2 wide
                is_wall = raw_maze[i][j:j+2] in [WALL, WALL_ALT]

                if raw_maze[i][j:j+2] == PLAYER:
                    self._player_pos = (i, j//2)

                if raw_maze[i][j:j+2] == FLAG:
                    self._flag_at = (i, j//2)

                n = Node((i, j//2), is_wall)
                line.append(n)


            self._maze.append(line)

    def __str__(self):
        s = ""

        if not hasattr(self, "_flag_at"):
            self._flag_at = (-1, -1)

        if not hasattr(self, "_player_pos"):
            self._player_pos = (-1, -1)

        for i in range(len(self._maze)):
            for j in range(len(self._maze[i])):

                if self._player_pos == (i, j): # show player over flag
                    s += PLAYER

                elif self._flag_at == (i, j):
                    s += FLAG

                else:
                    s += self._maze[i][j].render()  # from class node

            s += NEWLINE

        return s

    def ascii_render(self):
        s = str(self)
        return s.replace(WALL, WALL_ALT).replace(NEWLINE, NEWLINE_ALT)

    def get_player_pos(self):
        return self._player_pos

    def get_player_node(self):
        i, j = self._player_pos
        return self._maze[i][j]

    def get_flag_pos(self):
        return self._flag_at

    def get_flag_node(self):
        i, j = self._flag_at
        return self._maze[i][j]

    def get_actions(self, only_directions=True, pos=None):
        if pos is None:
            i, j = self._player_pos
        else:
            i, j = pos

        actions = ""
        nodes = []

        if not self._maze[i - 1][j].is_wall():
            actions += UP
            nodes.append(self._maze[i - 1][j])

        if not self._maze[i + 1][j].is_wall():
            actions += DOWN
            nodes.append(self._maze[i + 1][j])

        if not self._maze[i][j - 1].is_wall():
            actions += LEFT
            nodes.append(self._maze[i][j - 1])

        if not self._maze[i][j + 1].is_wall():
            actions += RIGHT
            nodes.append(self._maze[i][j + 1])

        if only_directions:
            return actions

        return zip(list(actions), nodes)

    def step(self, direction):
        if direction not in self.get_actions():
            return

        i, j = self._player_pos

        if direction == UP:
            self._player_pos = (i - 1, j)
        if direction == DOWN:
            self._player_pos = (i + 1, j)
        if direction == LEFT:
            self._player_pos = (i, j - 1)
        if direction == RIGHT:
            self._player_pos = (i, j + 1)

    def show_solve(self, way_to_flag):
        for direction in way_to_flag:
            system("clear")
            self.step(direction)
            print(self.__str__())
            sleep(0.1)

    def reset_solve(self):
        for line in self._maze:
            for node in line:
                node.reset()


class Node:
    def __init__(self, pos, is_wall=True):
        self._pos = pos
        self._is_wall = is_wall
        self._prev = "", None  # direction from prev_node to this node, prev_node
        self._dist = 2 ** 32   # Inf

    def get_pos(self):
        return self._pos

    def is_wall(self):
        return self._is_wall

    def clear_wall(self):
        self._is_wall = False

    def set_prev(self, direction, node):
        self._prev = (direction, node)

    def get_prev(self):
        return self._prev

    def set_dist(self, dist):
        self._dist = dist

    def get_dist(self):
        return self._dist

    def reset(self):
        self._prev = "", None
        self._dist = 2 ** 32

    def render(self):
        if self.is_wall():
            return WALL
        return CLEAR

    def __str__(self):
        return f"{self._pos} {self._dist}"


if __name__ == "__main__":
    from sys import argv

    m = Maze(verbose=True)
    m.step(m.get_actions()[0])
