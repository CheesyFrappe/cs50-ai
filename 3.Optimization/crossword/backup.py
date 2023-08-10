import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        #self.test()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
          
        for key, value in self.domains.items():
            temp = list()
            for word in value:
                if key.length == len(word):
                    temp.append(word)
            self.domains[key] = temp
       
    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if self.crossword.overlaps[x, y] == None:
            return None
        
        temp_list = list()
        i,j = self.crossword.overlaps[x, y]
        
        for word1 in self.domains[x]:
            flag = 0
            for word2 in self.domains[y]:
                if word1[i] == word2[j]:
                    flag = 1
                    break
                
            if flag:
                temp_list.append(word1)

        if self.domains[x] == temp_list:
            return None
        else:
            self.domains[x] = temp_list
            return True

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs == None:
            arcs = list()
            for v1 in self.domains:
                for v2 in self.domains:
                    if v1 != v2:
                        arcs.append((v1, v2))

        while len(arcs) != 0:
            x, y = arcs.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        arcs.append((neighbor, x))
        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        for var in self.crossword.variables:
            if var not in assignment.keys():
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        """
            all values are distinct, 
            every value is the correct length, 
            and there are no conflicts between neighboring variables.
        """
        distinct_list = list()

        for key, var in assignment:
            if var in distinct_list or key.length != len(var[0]):
                return False
            distinct_list.append(var[0])

        for key, var in assignment:
            for neighbor in self.crossword.neighbors(key):
                i, j = self.crossword.overlaps[key, neighbor]
                if var[0][i] != len(self.domains[neighbor][0][j]):
                    return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        temp = dict()
        ret_list = list()

        for value in self.domains[var]:
            counter = 0
            for node in assignment:
                if self.crossword.overlaps[var, node] != None or len(self.domains[node]) != 1:
                    if value in self.domains[node]:
                        counter+=1
            temp[value] = counter
        
        sorted_temp = sorted(temp.items(), key=lambda x:x[1])
        
        for val in sorted_temp:
            ret_list.append(val[0])
        return ret_list
    

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        temp_dict = dict()  # contains unassigned variables
        min_vals = list()   # containes unassigned variables with minimum number of values

        for key, val in self.domains.items():
            if key not in assignment.keys():
                temp_dict[key] = len(val)
        
        sorted_temp = sorted(temp_dict.items(), key=lambda x:x[1])
        #print(sorted_temp)
        min = sorted_temp[0][1]    # unassigned variable with minimum number of vals.

        for key, val in sorted_temp:
            if val == min:
                min_vals.append(key)

        if len(min_vals) == 1:
            return min_vals[0]
        
        count = 0
        for var in min_vals:
            if len(self.crossword.neighbors(var)) > count:
                count = len(self.crossword.neighbors(var))

        for var in min_vals:
            if len(self.crossword.neighbors(var)) == count:
                return var
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            #print(self.assignment_complete(assignment))
            return assignment
        var = self.select_unassigned_variable(assignment)

        for val in self.order_domain_values(var, assignment):
            assignment[var] = val
            result = self.backtrack(assignment)
            if result:
                return result
            del assignment[var] 
        return None


    def test(self):
        """
        for v1 in self.domains:
            for v2 in self.domains:
                if v1 == v2:
                    continue
                self.revise(v1, v2)
                #print(f"v1: {v1}\nv2: {v2}\nresult: {self.revise(v1, v2)}")
        """
        for var in self.crossword.variables:
            print(var)



def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
