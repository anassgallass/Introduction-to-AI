from pacman_module.game import Agent
from pacman_module.pacman import Directions

def key(state):

    return (state.getPacmanPosition(), state.getFood(), state.getGhostPosition(1))


class PacmanAgent(Agent):
    def __init__(self, args):
        self.args = args


    def maxv(self, state, player, closed):
        val = []
        curr_key = key(state)
        c = closed.copy()

        if curr_key in c:
            return c[curr_key] 

        else:
            c[curr_key] = float('-inf')
            for next_state,action in state.generatePacmanSuccessors():   
                value = self.minimax(next_state , 1, c)
                val = val + [value]

            c[curr_key] = max(val)
            return c[curr_key]        


    def minv(self, state, player, closed):
        val = []
        curr_key = key(state)
        c = closed.copy()

        if curr_key in c:
            return c[curr_key]

        else:
            c[curr_key] = float('inf')
            for next_state, action in state.generateGhostSuccessors(1):
                value = self.minimax(next_state , 0, c)     
                val = val + [value]

            c[curr_key] = min(val)
            return c[curr_key]


    def minimax(self, state, player, closed):
        """
        Given a pacman game state, , a player and a dictionnary, return
        a value 

        Arguments:
        ----------
        - 'state': the current game state.
        - 'player': 0 or 1 depending if the current player is pacman or Ghost
        - 'closed': a dictionnary helping avoiding cycles 

        Return:
        -------
        -  value helping to find the best path to terminal test
        """
        if state.isWin() or state.isLose():
            return state.getScore()

        if player == 0:
            return self.maxv(state, player, closed) 
        else:
            return self.minv(state, player, closed)

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
        
        tmp = float('-inf')

        for next_state, action in state.generatePacmanSuccessors():

            v = self.minimax(next_state, 1, dict()) # Pacman moves first
            
            if v >= tmp:
                tmp = v
                actionToPerform = action
  
        return actionToPerform