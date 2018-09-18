from copy import deepcopy


class OutOfBounds(Exception):
    pass


class BlackHole(Exception):
    pass


class InvalidMove(Exception):
    pass


class InvalidPreset(Exception):
    pass


class Node:
    def __init__(self, board, prev=None):
        self.board = board
        self.next = []
        self.prev = prev
        self.f = 0
        self.g = 0 if prev is None else prev.g + 1
        self.h = 0

    def calculate_h(self):
        h = 0
        for x in range(len(self.board.positions)):
            for y in range(len(self.board.positions[x])):
                if self.board.positions[x][y] > 0:
                    found = False
                    i = 0
                    j = 0

                    while not found and i <= 4:
                        if GOAL_STATE.positions[i][j] == self.board.positions[x][y]:
                            found = True
                        else:
                            j = j + 1
                            if j > 4:
                                j = j % 5
                                i = i + 1

                    if found:
                        h += abs(x - i) + abs(y - j)

        self.h = h
        self.f = self.g + self.h

    def generate_next(self):
        for move in self.board.generate_moves():
            self.next.append(Node(move, self))

    def update_node(self, new_version):
        self.prev = new_version.prev
        self.f = new_version.f
        self.g = new_version.g
        self.h = new_version.h


class BoardLayout:
    def __init__(self, move, pre=None):
        self.positions = [[], [], [], [], []]
        self.whitespace = ()

        if pre is not None:
            self.positions = deepcopy(pre.positions)

            x = pre.whitespace[0]
            y = pre.whitespace[1]

            try:
                if move == "u":
                    self.positions[x][y] = pre.positions[x - 1][y]
                    self.positions[x - 1][y] = pre.positions[x][y]
                    self.whitespace = (x - 1, y)
                elif move == "l":
                    self.positions[x][y] = pre.positions[x][y - 1]
                    self.positions[x][y - 1] = pre.positions[x][y]
                    self.whitespace = (x, y - 1)
                elif move == "d":
                    self.positions[x][y] = pre.positions[x + 1][y]
                    self.positions[x + 1][y] = pre.positions[x][y]
                    self.whitespace = (x + 1, y)
                elif move == "r":
                    self.positions[x][y] = pre.positions[x][y + 1]
                    self.positions[x][y + 1] = pre.positions[x][y]
                    self.whitespace = (x, y + 1)
                else:
                    raise InvalidMove
            except IndexError:
                raise OutOfBounds

            if self.whitespace[0] < 0 or self.whitespace[0] > 4 or self.whitespace[1] < 0 or self.whitespace[1] > 4:
                raise OutOfBounds
            elif self.positions[x][y] == -1:
                raise BlackHole

        elif move == "i":
            self.positions = [[2, 3, 7, 4, 5],
                              [1, -1, 11, -1, 8],
                              [6, 10, 0, 12, 15],
                              [9, -1, 14, -1, 20],
                              [13, 16, 17, 18, 19]]
            self.whitespace = (2, 2)
        elif move == "g":
            self.positions = [[1, 2, 3, 4, 5],
                              [6, -1, 7, -1, 8],
                              [9, 10, 0, 11, 12],
                              [13, -1, 14, -1, 15],
                              [16, 17, 18, 19, 20]]
            self.whitespace = (2, 2)
        else:
            raise InvalidPreset

    def __str__(self):
        string = ""
        for x in self.positions:
            for y in x:
                string += str(y) + "\t"
            string += "\n"
        return string

    def equals(self, test):
        for x in range(len(self.positions)):
            for y in range(len(self.positions[x])):
                if self.positions[x][y] != test.positions[x][y]:
                    return False
        return True

    def generate_moves(self):
        moves = []

        for direction in ["l", "u", "r", "d"]:
            try:
                move = BoardLayout(direction, self)
                moves.append(move)
            except (OutOfBounds, BlackHole):
                continue

        return moves


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def is_empty(self):
        return len(self.queue) == 0

    def enqueue(self, node):
        self.queue.append(node)

    def dequeue(self):
        index = -1
        for i in range(len(self.queue)):
            if index < 0 or self.queue[i].f < self.queue[index].f:
                index = i

        if index > -1:
            node = self.queue[index]
            del self.queue[index]
            return node

    def find(self, node):
        for _node in self.queue:
            if _node.board.equals(node.board):
                return _node
        return None

    def remove(self, node):
        for i in range(len(self.queue)):
            if self.queue[i].board.equals(node.board):
                del self.queue[i]


GOAL_STATE = BoardLayout("g")


def display_results(successful_node, closed_queue):
    print("Congratulations! You won!")
    print()
    print("Steps taken to complete: " + str(successful_node.g))
    print("Total states explored: " + str(len(closed_queue)))
    print()
    print("Fifth State:\n" + str(closed_queue[5].board))
    print("Fifth-to-Last State:\n" + str(closed_queue[len(closed_queue) - 5].board))
    exit()


def display_failure():
    print("You failed. RIP")
    exit()


def main():
    open_queue = PriorityQueue()
    closed_queue = PriorityQueue()

    open_queue.enqueue(Node(BoardLayout("i")))

    while not open_queue.is_empty():
        node = open_queue.dequeue()
        closed_queue.enqueue(node)

        if node.board.equals(GOAL_STATE):
            display_results(node, closed_queue.queue)

        node.generate_next()
        for next_node in node.next:
            open_node = open_queue.find(next_node)
            closed_node = closed_queue.find(next_node)

            if open_node is None and closed_node is None:
                next_node.calculate_h()
                open_queue.enqueue(next_node)
            elif open_node is not None and next_node.g < open_node.g:
                open_node.update_node(next_node)
            elif closed_node is not None and next_node.g < closed_node.g:
                closed_node.remove(closed_node)
                open_queue.enqueue(next_node)

    display_failure()


if __name__ == "__main__":
    main()
