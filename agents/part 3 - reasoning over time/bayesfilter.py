# Complete this class for all parts of the project

from pacman_module.game import Agent
import numpy as np
from pacman_module import util
from scipy.stats import binom


class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        """
            Variables to use in 'update_belief_state' method.
            Initialization occurs in 'get_action' method.
        """
        # Current list of belief states over ghost positions
        self.beliefGhostStates = None

        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None

        # Hyper-parameters
        self.ghost_type = self.args.ghostagent
        self.sensor_variance = self.args.sensorvariance

        self.p = 0.5
        self.n = int(self.sensor_variance/(self.p*(1-self.p)))

    def nb0fGhostLegalMoves(self, i, j):
        
        ghostlegalmoves = 0

        if(not self.walls[i-1][j]):
            ghostlegalmoves+=1
        if(not self.walls[i+1][j]):     
            ghostlegalmoves+=1
        if(not self.walls[i][j+1]):
            ghostlegalmoves+=1
        if(not self.walls[i][j-1]):
            ghostlegalmoves+=1

        return ghostlegalmoves

    def transition_model(self, x_now, y_now, x_next, y_next, pacman_position):
        
        dist = util.manhattanDistance((x_now, y_now), (x_next, y_next))
        if dist != 1:
            return 0

        if self.walls[x_now][y_now] or self.walls[x_next][y_next]:
            return 0

        if self.ghost_type == "confused":
            
            nb_of_moves = self.nb0fGhostLegalMoves(x_now, y_now)
            proba=1/nb_of_moves
            return proba

        if self.ghost_type == "afraid":
            
            distrib = util.Counter()
            CellPosition=(x_now,y_now)
            CellDistance=util.manhattanDistance(pacman_position,CellPosition)
            if(not self.walls[x_now-1][y_now]):
                LeftDistance=util.manhattanDistance(pacman_position,(x_now-1,y_now)) 
                if(CellDistance<=LeftDistance):
                    distrib[(x_now -1 , y_now)]=2
                else:
                    distrib[(x_now -1 , y_now)]=1
            
            if(not self.walls[x_now+1][y_now]):
                RightDistance=util.manhattanDistance(pacman_position,(x_now+1,y_now))
                if(CellDistance<=RightDistance):
                    distrib[(x_now + 1 , y_now)]=2
                else:    
                    distrib[(x_now + 1 , y_now)]=1
            
            if(not self.walls[x_now][y_now-1]):
                DownDistance = util.manhattanDistance(pacman_position,(x_now,y_now-1))
                if(CellDistance<=DownDistance):
                    distrib[(x_now , y_now - 1)]=2
                else:
                    distrib[(x_now , y_now - 1)]=1
            
            if(not self.walls[x_now][y_now+1]):
                UpDistance=util.manhattanDistance(pacman_position,(x_now,y_now+1))
                if(CellDistance<=UpDistance):
                    distrib[(x_now , y_now + 1)]=2
                else:    
                    distrib[(x_now , y_now + 1)]=1

            distrib.normalize()
            return distrib[(x_next, y_next)]

        if self.ghost_type == "scared":

            distrib = util.Counter()
            CellPosition=(x_now,y_now)
            CellDistance=util.manhattanDistance(pacman_position,CellPosition)
            if(not self.walls[x_now-1][y_now]):
                LeftDistance=util.manhattanDistance(pacman_position,(x_now-1,y_now)) 
                if(CellDistance<=LeftDistance):
                    distrib[(x_now - 1 , y_now )]=8
                else:
                    distrib[(x_now - 1 , y_now )]=1
            if(not self.walls[x_now+1][y_now]):
                RightDistance=util.manhattanDistance(pacman_position,(x_now+1,y_now))
                if(CellDistance<=RightDistance):
                    distrib[(x_now + 1 , y_now )]=8
                else:
                    distrib[(x_now + 1 , y_now )]=1
            if(not self.walls[x_now][y_now-1]):
                DownDistance = util.manhattanDistance(pacman_position,(x_now,y_now-1))
                if(CellDistance<=DownDistance):
                    distrib[(x_now , y_now - 1)]=8
                else:
                    distrib[(x_now , y_now - 1)]=1
            if(not self.walls[x_now][y_now+1]):
                UpDistance=util.manhattanDistance(pacman_position,(x_now,y_now+1))
                if(CellDistance<=UpDistance):
                    distrib[(x_now , y_now + 1)]=8
                else:
                    distrib[(x_now , y_now + 1)]=1

            distrib.normalize()
  
            return distrib[(x_next, y_next)]



    def sensor_model(self, evidence, ghost_position, pacman_position):
        
        distance=util.manhattanDistance(pacman_position,ghost_position)
        return binom.pmf(evidence + self.n*self.p, self.n, self.p, loc=distance)



    def update_belief_state(self, evidences, pacman_position, ghosts_eaten):
        
        beliefStates = self.beliefGhostStates

        # XXX: Your code here
        
         

        N = self.walls.width
        M = self.walls.height

    
        
        for index in range(0, len(evidences)):
            mat = np.zeros((N,M))
            #mat is the "Total transition matrix"
            for i in range(0,N):
                for j in range(0, M): 
                    for n in range(0, N):
                        for m in range(0, M):
                            mat[i][j] += self.transition_model(n,m, i, j, pacman_position)*self.beliefGhostStates[index][n][m]
            

            for j in range(0, M):
                for i in range(0, N):
                    beliefStates[index][i][j] =  self.sensor_model(evidences[index], (i,j), pacman_position)*mat[i][j]
            alpha=beliefStates[index].sum()
            for j in range(0,M):
                for i in range(0,N):
                    if(alpha!=0):
                        beliefStates[index][i][j]=beliefStates[index][i][j]/alpha
            

        # XXX: End of your code

        self.beliefGhostStates = beliefStates

        return beliefStates

    def _get_evidence(self, state):
        """
        Computes noisy distances between pacman and ghosts.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.


        Return:
        -------
        - A list of Z noised distances in real numbers
          where Z is the number of ghosts.

        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """

        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []

        for pos in positions:
            true_distance = util.manhattanDistance(pos, pacman_position)
            rvs = binom.rvs(self.n, self.p)
            espérance = self.n*self.p
            noise = rvs - espérance
            noisy_distances.append(true_distance + noise)

        return noisy_distances

    def _record_metrics(self, belief_states, state):
        """
        Use this function to record your metrics
        related to true and belief states.
        Won't be part of specification grading.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.
        - `belief_states`: A list of Z
           N*M numpy matrices of probabilities
           where N and M are respectively width and height
           of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """
        pass

    

    def get_action(self, state):
        """
        Given a pacman game state, returns a belief state.

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A belief state.
        """

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()

        evidence = self._get_evidence(state)
        newBeliefStates = self.update_belief_state(evidence,
                                                   state.getPacmanPosition(),
                                                   state.data._eaten[1:])
        self._record_metrics(self.beliefGhostStates, state)

        return newBeliefStates, evidence