class Board:
    def __init__(self):
        self.spaces = []
        self.current_row = 0

        for _ in range(25):
            row = []
            for _ in range(25):
                row.append(0)
            self.spaces.append(row)

    def __str__(self):
        string = ""

        for row in self.spaces:
            for space in row:
                if space > 0:
                    string += "Q"
                elif space < 0:
                    string += "X"
                else:
                    string += "_"
                string += " "
            string += "\n"

        return string

    def add_queen(self, col=0):
        if col >= len(self.spaces[self.current_row]):
            return False
        elif self.spaces[self.current_row][col] == 0:
            self.spaces[self.current_row][col] = 1

            for i in range(len(self.spaces[self.current_row])):
                if i != col:
                    self.spaces[self.current_row][i] -= 1
            for i in range(len(self.spaces)):
                if i != self.current_row:
                    self.spaces[i][col] -= 1

            for i in range(4):
                x = self.current_row + (1 if i & 1 else -1)
                y = col + (1 if i & 2 else -1)
                while 0 <= x < 25 and 0 <= y < 25:
                    self.spaces[x][y] -= 1

                    x += (1 if i & 1 else -1)
                    y += (1 if i & 2 else -1)

            self.current_row += 1
            #print(self)
            return True
        elif col + 1 < len(self.spaces[self.current_row]):
            return self.add_queen(col + 1)
        else:
            return False

    def backtrack(self):
        #print(self)
        self.current_row -= 1

        index = -1
        for i in range(len(self.spaces[self.current_row])):
            if self.spaces[self.current_row][i] > 0:
                index = i
                self.spaces[self.current_row][i] = 0
                break

        if index > -1:
            for i in range(len(self.spaces)):
                if i != self.current_row:
                    self.spaces[i][index] += 1
            for i in range(len(self.spaces[self.current_row])):
                if i != index:
                    self.spaces[self.current_row][i] += 1

            for i in range(4):
                x = self.current_row + (1 if i & 1 else -1)
                y = index + (1 if i & 2 else -1)
                while 0 <= x < 25 and 0 <= y < 25:
                    self.spaces[x][y] += 1

                    x += (1 if i & 1 else -1)
                    y += (1 if i & 2 else -1)

            return index


def main():
    game_board = Board()

    queens_placed = 0
    to_start = 0
    while queens_placed < 25:
        if not game_board.add_queen(to_start):
            to_start = game_board.backtrack() + 1
            queens_placed -= 1
        else:
            to_start = 0
            queens_placed += 1

    print(game_board)


if __name__ == "__main__":
    main()
