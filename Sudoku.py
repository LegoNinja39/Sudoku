from random import shuffle, random

# Driving class
class Board:
    def __init__(self, size=3, path="") -> None:
        if path.strip():
            self.board = []
            with open(path) as f: self.board.extend(map(lambda x: [int(i) for i in x], (l.split() for l in f)))
            self.nBox = int(len(self.board)**0.5)
        else:
            self.nBox = size
            s=size*size
            # 0 is used to indicate empty
            self.board = [[0 for _ in range(s)] for _ in range(s)]
        self._mxpos = len(self) - 1
        self.nOrder = [i for i in range(1, len(self) + 1)]
        shuffle(self.nOrder)
    
    # Show overriding builtin operator
    def __len__(self):
        return len(self.board)

    # Show read-only property
    @property
    def MAX_POS(self) -> int:
        return self._mxpos

    # Show str
    def __str__(self):
        dashRow = "- " + " - ".join(("-"*5 for _ in range(3))) + " -\n"
        display = dashRow
        for x, row in enumerate(self.board):
            if x % 3 == 0 and x != 0: display += dashRow
            for y, col in enumerate(row):
                if y % 3 == 0: display += "| "
                display += str(col) + " " if col else "  " # Makes 0s blanks
            display += "|\n"
        display += dashRow
        return display
    
    # Write board to file
    def writeBoard(self, path: str):
        with open(path, mode="w") as f:
            for i in self.board:
                f.write(" ".join(map(str, i)) + "\n")

    # Moves the iterator one space
    def nextSpace(self, cp: tuple, forward=True) -> tuple[int, int]:
        x = cp[0]; y = cp[1] # Show ; in Python
        # Move forward
        if forward:
            # If it reaches the end of the row
            #   wrap around
            y = y + 1 if y < self.MAX_POS else 0 # Ternary
            if not y: x += 1 # if y==0: row++
        # Move back
        else:
            # If it reaches the beginning of the row
            #   wrap around
            y = y - 1 if y else self.MAX_POS # Ternary
            if y == self.MAX_POS: x -= 1
        return (x, y)
    
    # Checks a specific number can be placed in a specific location
    def checkNum(self, n: int, cp: tuple) -> bool:
        # Numbers cannot repeat in a row
        if n in self.board[cp[0]]: return False
        # Numbers cannot repeat in a column
        elif n in [r[cp[1]] for r in self.board]: return False
        # Gets all the numbers in a box
        # boxIndex=x//boxSize; boxStart=boxIndex*numBoxes; element=boxStart*index
        elif n in (self.board[(cp[0]//self.nBox)*self.nBox+i][(cp[1]//self.nBox)*self.nBox+j] for j in range(self.nBox) for i in range(self.nBox)): return False
        else: return True

    # Recusively places numbers in the board
    def placeNum(self, cp: tuple[int, int]):
        # If the next row is past the board, all the numbers have been placed
        if cp[0] > self.MAX_POS: return True
        # Searches for the next 0 square
        while self.board[cp[0]][cp[1]]: 
            cp = self.nextSpace(cp)
            if cp[0] > self.MAX_POS: return True # Breaks if the bottom is reached
        for n in self.nOrder:
            if self.checkNum(n, cp):
                self.board[cp[0]][cp[1]] = n
                if self.placeNum(self.nextSpace(cp)): break
        else: # This will run if none of the numbers can be placed
            self.board[cp[0]][cp[1]] = 0
            return False
        return True

def build(bFile: str):
    print("\n*** Sudoku Maker ***")
    nb = Board()
    nb.placeNum((0,0))
    nb.writeBoard(bFile)
    print(nb)

def remove(bFile: str, r: int):
    print("\n*** Removing Numbers ***")
    rb = Board(path=bFile)
    for coord in ((max(0, int(random()*10)-1), max(0, int(random()*10)-1)) for _ in range(r)): rb.board[coord[0]][coord[1]] = 0
    rb.writeBoard(bFile)
    print(rb)

def solve(bFile: str):
    print("\n*** Sudoku Solver ***")
    sb = Board(path=bFile)
    sb.placeNum((0,0))
    sb.writeBoard(bFile)
    print(sb)