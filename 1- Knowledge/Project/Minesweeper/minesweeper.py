import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count != 0: 
            return self.cells 
        else: 
            return set() 

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0: 
            return self.cells 
        else: 
            return set() 

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells: 
            self.cells.remove(cell)
            self.count = self.count - 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells: 
            self.cells.remove(cell) 


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # mark moves made as safe 
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # temporary sentence set to add to knowledge 
        new_sentence = set() 

        # look at neighbouring cells 
        for i in range(cell[0] - 1, cell[0] + 2): 
            for j in range(cell[1] - 1, cell[1] + 2): 
                # ignore cell 
                if (i, j) == cell: 
                    continue 

                # ignore safe cells 
                if (i, j) in self.safes: 
                    continue 

                # ignore mines, and subtract count by one 
                if (i, j) in self.mines: 
                    count -= 1 
                    continue 
                # otherwise, add undetermined cells to sentence 
                if 0 <= i < self.height and 0 <= j < self.width: 
                    new_sentence.add((i, j))

        # add sentences to knowledge base 
        self.knowledge.append(Sentence(new_sentence, count))

        # update knowledge 
        new_info = True 

        while new_info: 
            new_info = False 

            safes = set() 
            mines = set() 

            # acquire current safes and mines 
            for sentence in self.knowledge: 
                safes = safes.union(sentence.known_safes())
                mines = mines.union(sentence.known_mines())

            # mark safes or mines 
            if safes: 
                new_info = True 
                for safe in safes: 
                    self.mark_safe(safe) 
            
            if mines: 
                new_info = True 
                for mine in mines: 
                    self.mark_mine(mine) 

            # remove empty sentences 
            empty = Sentence(set(), 0) 
            self.knowledge[:] = [x for x in self.knowledge if x != empty] 

            # inferring new sentences from current 
            for sentence_1 in self.knowledge: 
                for sentence_2 in self.knowledge: 

                    # ignore identical sentences 
                    if sentence_1.cells == sentence_2.cells: 
                        continue 

                    # create new sentence if 1 is subset of 2 and not in current knowledge 
                    if sentence_1.cells.issubset(sentence_2.cells): 
                        new_cells = sentence_2.cells - sentence_1.cells 
                        new_count = sentence_2.count - sentence_1.count 

                        new_sentence = Sentence(new_cells, new_count) 

                        # add to knowledge 
                        if new_sentence not in self.knowledge: 
                            new_info = True 
                            self.knowledge.append(new_sentence)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        
        if safe_moves: 
            # set of all safe moves 
            safe_moves = self.safes - self.moves_made
            # pick one of them 
            pick = random.choice(list(safe_moves))
            return pick 
        else: 
            return None 
    

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # make sure move made is within bounds 
        width = set(range(self.width + 1)) 
        height = set(range(self.height + 1)) 

        # subtract moves made 
        for tuple in self.moves_made: 
            i = tuple[0] 
            if i in width: 
                width.remove(i)
        for tuple in self.moves_made: 
            j = tuple[1] 
            if j in height: 
                height.remove(j) 

        # subtract mines 
        for tuple in self.mines: 
            i = tuple[0] 
            if i in width: 
                width.remove(i) 
        for tuple in self.mines: 
            j = tuple[1]
            if j in height: 
                height.remove(j)

        # if no coordinates exist, return None, otherwise return random tile 
        if not width or not height: 
            return None 
        else:             
            random_x = random.choice(list(width))
            random_y = random.choice(list(height)) 
            return (random_x, random_y)
