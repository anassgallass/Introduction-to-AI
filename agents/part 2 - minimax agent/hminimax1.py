import imp
import os
from argparse import ArgumentParser, ArgumentTypeError

from pacman_module.game import *
from pacman_module.pacman import *
from pacman_module.util import *

#global variable helping to avoid cycles
global visitedState 
visitedState = dict()

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
    return (state.getPacmanPosition(), state.getFood(), state.getGhostPosition(1))


class PacmanAgent(Agent):
    def __init__(self, args):
        self.args = args

    def fullPathFood(self, state, positionP, positionG, foodList):

        """
        Returns a distance.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
               `pacman.GameState`.
        - `PositionP`: the current position of Pacman
        - `PositionG`: the current position of the Ghost
        - `foodList`: the matrix state.getFood() turned as a list



        Return:
        -------
        - A total distance going through every node
        """
        allDistances = []

        for i in range(len(foodList)):
            allDistances = allDistances + [manhattanDistance(positionP, foodList[i])]

        if len(allDistances) == 0:
            return 1E-10
        fullPathFood = min(allDistances)
        
        while len(foodList) > 1:
            i = allDistances.index(min(allDistances))
            nearest = foodList[i]
            foodList.remove(foodList[i])
            allDistances = []

            for i in range(len(foodList)):
                dist = manhattanDistance(nearest, foodList[i])
                allDistances = allDistances + [dist]

            fullPathFood = fullPathFood + min(allDistances)

        return fullPathFood

    def eval1(self, state):

        """
        Returns an evaluation of a given state.

        Arguments:
        ----------
        - 'state': the current game state.


        Return:
        -------
        - The value of the evaluation.
        """
        
        positionP = state.getPacmanPosition()  #position of Pacman
        positionG = state.getGhostPosition(1)  #position of Ghost    

        foodList = state.getFood().asList()
        lengthList = len(foodList)        
        distance = []
        for i in range(lengthList):
            distance = distance + [manhattanDistance( positionP, foodList[i])]

        #distance between Pacman and Food
        dist_P_F = 0
        if len(distance) > 0:
            dist_P_F = min(distance)
        
        #distance between Pacman and Ghost
        dist_P_G = manhattanDistance( positionP, positionG) 

        #distance between two dots
        fullPathFood= self.fullPathFood(state, positionP, positionG, foodList)

        #evaluatation function 
        evalValue = state.getScore() - dist_P_F +dist_P_G - fullPathFood

        return evalValue



    def maxv(self, state, player, closed, depth):

        val = []
        curr_key = key(state)
        c = closed.copy()

        if curr_key in c:
            return c[curr_key] 
    
        #for avoiding cycles
        if curr_key in visitedState:
            return float("-inf")

        else:
            c[curr_key] = float('-inf')
            for next_state,action in state.generatePacmanSuccessors():   
                value = self.hminimax(next_state , 1, c, depth + 1)
                val = val + [value]

            c[curr_key] = max(val)
            return c[curr_key]        

    def minv(self, state, player, closed, depth):

        val = []
        curr_key = key(state)
        c = closed.copy()

        if curr_key in c:
            return c[curr_key]
        
        #for avoiding cycles
        if curr_key in visitedState:
            print("minv")
            return float("inf")


        else:
            c[curr_key] = float('inf')
            for next_state, action in state.generateGhostSuccessors(1):
                value = self.hminimax(next_state , 0, c, depth + 1)     
                val = val + [value]

            c[curr_key] = min(val)
            return c[curr_key]
    
    def cutoffTest(self, state, depth):
        
            if depth == 3 or state.isWin() or state.isLose():
                return True
            else:
                return False

    def hminimax(self, state, player, closed, depth):

        """
        Returns the best reachable value from that state.

        Arguments:
        ----------
        - 'state': the current game state.
        - 'player': the player that has to make the move.
        - 'closed': the closed set that contains states we've been through.
        - 'depth': the current depth of the recursion.


        Return:
        -------
        - A value.
        """
        if self.cutoffTest(state, depth) == True:
            return self.eval1(state)

        if player == 0:
            return self.maxv(state, player, closed, depth) 
        else:
            return self.minv(state, player, closed, depth)

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
            v = self.hminimax(next_state, 1, dict(), 1) 
            if v >= tmp:
                tmp = v
                actionToPerform = action

        global visitedState
        visitedState[key(state)] = tmp

        return actionToPerform