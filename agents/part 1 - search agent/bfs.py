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
                self.moves = self.bfs(state)

        try:
            return self.moves.pop(0)

        except IndexError:
            return Directions.STOP



    def h(self, state):
        
        return 0
    
    def g(self, state, next_state):

        return 0


    def bfs(self, state):
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