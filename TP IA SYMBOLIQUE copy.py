# TP IA SYMBOLIQUE
# 22203313 - Ruscu Oana Maria (Erasmus)
# 22202055 - Somarandy Adrien

# Game Elements

class cube():
    """Class representing a cube in the game. A cube has a number
    and eventually a weight (default weight = 1)"""

    def __init__(self, num, weight=1):
        self.num = num
        self.weight = weight

    def get_num(self):
        """Function returning the number of the cube
        Input : None
        Output : int for the number of the cube"""
        return self.num


class pike():
    """Class representing a pike in the game. A pike is a list of cubes
    with a minimal length of 0 and a maximal length of 3."""

    def __init__(self, number_cube=0, cubes=None):
        if (cubes != None):
            self.cubes = cubes
        else:
            self.cubes = []
        self.number_cube = number_cube

    def get_cube(self):
        """Function returning the cube at the head of the pike
        Input : None
        Ouput : cube object"""
        return self.cubes[self.number_cube-1]

    def add_cube(self, cube):
        """Function adding a cube on the pike
        Input : cube object
        Output : None"""
        self.cubes.append(cube)

    def is_full(self):
        """Function returning a boolean representing the filling of a pike
        Input : None
        Output : Boolean"""
        return self.number_cube == 3

    def pike_to_list(self):
        """Function converting a pike into a list of number 
        for easy manipulations
        Input : None
        Output : list of int"""
        res = []
        for i in range(len(self.cubes)):
            res.append(self.cubes[i].get_num())
        return res


class rumba():
    """Class representing the entire game. The game is composed of 4 pikes, 
    each pike can contain at most 3 cubes. Can create a game from nothing or
    from the structure of a current game (List of pikes)"""

    def __init__(self, current=None, random_weight=False):
        if (random_weight):
            print("Non implémenté")
        if (current != None):
            self.game = current
        else:
            # creating a starting game
            self.game = []
            for i in range(3):
                cubes = []
                for j in range(i+1, i+5):
                    cubes.append(cube(j, 1))
                self.game.append(pike(3, cubes))
            self.game.append(pike())

    def get_cube(self, nPike):
        """Function getting the last cube on the pike
        Input : int of the pike
        Output : cube object on the head of the pike"""
        return self.game[nPike].get_cube()

    def add_cube(self, cube, nPike):
        """Function adding a cube on the pike
        Input : object cube, int of the pike
        Output : None"""
        self.game[nPike].cubes.append(cube)
        self.game[nPike].number_cube += 1

    def move_cube(self, p1, p2):
        """Function moving the cube at the head of p1 to p2
        Input : int for the origin pike, int for the new pike
        Output : None"""
        cube = self.game[p1].cubes.pop()
        self.game[p1].number_cube -= 1
        self.add_cube(cube, p2)

    def print_state(self):
        """Function printing the state of the game
        Input : None
        Output : None"""
        # structure : game[[level0],[level1],[level2]]
        res = [[" ", " ", " ", " "], [" ", " ", " ", " "], [" ", " ", " ", " "]]
        for i in range(3):
            for j in range(4):
                if self.game[j].number_cube > i:
                    res[i][j] = (self.game[j].cubes[i].get_num())
        for i in reversed(range(3)):
            for j in res[i]:
                print(j, end=' ')
            print("")
        print("_______")

    def game_to_list(self):
        """Function converting the game into a matrix of int
        for easy manipulation
        Input : None
        Output : Matrix of int"""
        res = []
        for i in self.game:
            res.append(i.pike_to_list())
        return res


def matrix_to_game(m):
    """Function converting the matrix into a game object
    Input : matrix of int
    Output : rumba object"""
    game = []
    for i in m:
        cubes = []
        number_of_cube = len(i)
        for j in range(number_of_cube):
            cubes.append(cube(i[j]))
        game.append(pike(number_of_cube, cubes))
    return rumba(game)


# Fonctions annexes pour la recherche

def find_destination(s, pi):
    # pi : pique initial dans le jeu (indice dans la liste = pi-1)
    """Fonction creating a list of the pikes we can reach from the
    initial pike
    Input : Matrix of the current game, int for the origin pike
    Output : list of int"""
    result = []
    if pi-2 < 0:
        pred = None
    else:
        pred = pi-2
    if pi == 4:
        next = None
    else:
        next = pi
    for i in [pred, next]:
        if i != None:
            if len(s[i]) < 3:
                result.append(i)
    return result


def move(s, p1, p2):
    """Function moving a cube from p1 to p2 in a matrix of a game
    Input : Matrix of the current game, int for the origin, int for the destination
    Output : Matrix of the new game"""
    g = matrix_to_game(s)
    g.move_cube(p1-1, p2-1)
    return g.game_to_list()


def is_goal(e):
    """Function returning a boolean representing
    if it's the goal (global variable)
    Input : Matrix of int
    Output : Boolean"""
    return differences(e) == 0


def opPoss(s):
    """Function returning a list of tuple representing the possible
    operations from the current game. Each tuple follows the structure
    (couple of int representing the move, matrix representing the new game, the cost)
    Input : Matrix of the current game
    Output : List of tuple"""
    res = []
    for i in range(4):
        pikes = find_destination(s, i+1)
        for j in range(len(pikes)):
            res.append(((i+1, pikes[j]+1), move(s, i+1, pikes[j]+1), 1))
    return res


def differences(s):
    """Function computing the number of differences between the current
    game and the goal
    Input : Matrix of the current game
    Output : int for the number of differences"""
    differences = 0
    for i in range(4):
        ps = s[i].copy()
        pg = goal[i].copy()
        while len(ps) != 3:
            ps.append('')
        while len(pg) != 3:
            pg.append('')
        for j in range(3):
            if ps[j] != pg[j]:
                differences += 1
    return differences


def h(s):
    """Function returning the cost from the current game to the goal
    Input : Matrix of the current game
    Output : int for the cost"""
    return differences(s)


def heuristic(s, g):
    """Function computing the heuristic for the current game
    Input : Matrix of the current game, cost since the beginning
    Output : int for the heuristic"""
    return g+h(s)


# Fonctions de recherche

def idaStarSearch(start, g):
    """Function realizing the search of the path from a current game to
    the goal following the IDA Star algorithm
    Input : Matrix of the current game, initial heuristic
    Output : Matrix of the solution (need to be modified)"""
    limit = heuristic(start, g)
    print(limit)
    finished = False
    solution = []
    # Starting the bounded depth exploration
    while not finished:
        # counter_g = 0
        nLimit = float('inf')
        saw = []
        queue = [("", start, "")]
        iteration = 0
        step = 0
        while queue and iteration < 6000:  # Si queue non vide -> True
            # Lecture de la queue comme une pile, donc utilisation de pop
            print("Try n°", iteration)
            next = queue.pop()
            saw.append(next)
            if next[0] != "":
                print("Move : ", next[0], ", Cost : <",
                      g, ",", h(next[1]), ">")
                print("Current State")
                matrix_to_game(next[1]).print_state()
                print()
            if is_goal(next[1]):
                print("Found goal")
                solution = next
                finished = True
                break
            else:
                print("Searching in possible operations")
                # excounter = counter_g
                for s in opPoss(next[1]):
                    counter_g = heuristic(s[1], g)
                    if h(s[1]) <= limit and not s in saw:
                        queue.append(s)
                    else:
                        nLimit = min(nLimit, h(s[1]))
            iteration += 1
            g += 1
            print()
        if iteration >= 6000:
            print("Search limit reached")
        if nLimit == float('inf'):
            print("nLimit == +inf")
            finished = True
            break
        else:
            limit = nLimit
            finished = False
            break
    # Ending bounded depth exploration
    # Problem with the heuristic and the print of the moves
    return solution


# Testing variables
global goal, init
goal1 = [[3, 2, 1], [], [6, 5, 4], [9, 8, 7]]
goal2 = [[3, 2, 1], [9, 8, 7], [6, 5, 4], []]
init1 = [[3, 2], [1], [6, 5, 4], [9, 8, 7]]
init2 = [[3, 2, 1], [6, 5, 4], [9, 8, 7], []]
goal3 = [[3, 2, 7], [6, 4, 8], [9, 5, 1], []]
goal4 = [[3, 1, 2], [6, 4, 5], [9, 7, 8], []]
goal5 = [[3, 2, 8], [6, 4], [9, 7, 5], [1]]
goal6 = [[4, 7, 1], [5, 8, 2], [6, 9, 3], []]
goal7 = [[], [1, 2, 3], [6, 5, 4], [9, 8, 7]]
goal8 = [[3, 2, 1], [4, 5, 6], [], [9, 8, 7]]
goal = goal7
init = init2

# Utilization of the algorithm
# Starting
print("Starting the game")
print("Initial case")
game = matrix_to_game(init)
game.print_state()
print("Start the search")
current = init
g = 0
res = idaStarSearch(current, g)
print()
if not res:
    print("empty list")
else:
    print(res)
    print()
    tmp = matrix_to_game(res[1])
    tmp.print_state()
print()
print("End of the game")

####################### Tests #####################
# game_test = rumba([pike(1, [cube(1)]), pike(2, [cube(2), cube(3)]), pike(
#    3, [cube(4), cube(5), cube(6)]), pike(3, [cube(7), cube(8), cube(9)])])
# game_test2 = matrix_to_game([[1], [2, 3], [4, 5, 6], [7, 8, 9]])
# game_test2.print_state()
# print(game_test.game[1].pike_to_list())
