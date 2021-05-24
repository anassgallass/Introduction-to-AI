from pacman_module.game import *
from pacman_module.pacman import *
from pacman_module.util import *

def key(state):
    """
    Returns a key that uniquely identifies a Pacman game state.

    Arguments:
    ----------
    - `state`: the current game state. See FAQ and class
               `pacman.GameState`.

    Return:
    -------
    - A hashable key object that uniquely identifies a Pacman game state.
    """
    return (state.getPacmanPosition(), state.getFood())

class PacmanAgent(Agent):
    """
    A Pacman agent based on A*.
    """
    def __init__(self, arg):
        """
        Arguments:
        ----------
        - 'args': Namespace of arguments from command-line prompt.
        """
        self.moves = []        

 

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.

        Arguments:
        ----------
        - 'state': the current game state.

        Return:
        -------
        - A legal move as defined in 'game.Directions'.
        """
        if not self.moves:
                self.moves = self.astar(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP



    def h(self, state):
        """
        Given a pacman game state, returns the manhattan distance of the furthest food

        Arguments:
        ----------
        - 'state': the current game state.

        Return:
        -------
        - the manhattan distance between the furthest food and the pacman position
        """
        foodList = state.getFood().asList()
        lengthList = len(foodList)        
        distance = [0 for i in range(lengthList)]
        for i in range(lengthList):
             distance[i] = manhattanDistance( state.getPacmanPosition() , foodList[i])

        if len(distance) == 0:
            return 0
        return max(distance)

    def g(self, state, next_state):
        """
        Given a pacman game state and its next game state, returns the  cost path

        Arguments:
        ----------
        - 'state': the current game state.
        - 'next_state': the next game state

        Return:
        -------
        - the cost path
        """
        if next_state.getPacmanPosition() in state.getCapsules():
            g = 6
        else:
            g = 1
        return g


    def astar(self, state):
        """
        Given a pacman game state,
        returns a list of legal moves to solve the search layout.

        Arguments:
        ----------
        - `state`: the current game state.
        
        Return:
        -------
        - A list of legal moves as defined in `game.Directions`.
        """
        path = []
        fringe = PriorityQueue()
        fringe.push((state, path, 0), 0)
        closed = set()

        while True :

            if fringe.isEmpty():
                return [] #failure

            priority, (current, path, cost) = fringe.pop()
            
            if current.isWin():
                return path

            currentKey = key(current)

            if currentKey not in closed:
                closed.add(currentKey)

                for next_state, action in current.generatePacmanSuccessors(): 
                    g = self.g(current, next_state) + cost

                    f = g + self.h(next_state)

                    fringe.push((next_state, path + [action], g), f)

        return path
