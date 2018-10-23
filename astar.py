from pacman_module.game import Agent
from pacman_module.pacman import Directions
from pacman_module.util import PriorityQueue
import math

class PacmanAgent(Agent):

    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args
        self.nextactions = list() #List to contain the final path to the goal
    
    def nullHeuristic(self, state):
        """
        Implementation of a trivial heuristic.
        """
        return 0

    def manhattan_distance(self, current, goal):
        """
        Compute the manhattan distance between two tuples of coordinates.
        Arguments:
        ----------
        - `current`: a tuple of coordinates of a starting point.
        - `goal` : a tuple of coordinates of a goal point.
        Return:
        -------
        - The manhattan distance between the starting point and the goal point.
        """
        dx = abs(current[0] - goal[0])
        dy = abs(current[1] - goal[1])
        return dx + dy

    def manhattan_maximum(self, state):
        """
        Given a pacman state, computes the maximum manhattan distance between
        that state and all the leftover foods.
        Arguments:
        ----------
        - `state`: the current game state.
        Return:
        -------
        - The biggest manhattan distance from the current state to all the left foods.
        """
        max_man = 0
        x, y = state.getPacmanPosition()
        current_food = state.getFood()

        #For each position check if there is food or not
        for i in range(current_food.width):
            for j in range(current_food.height):
                if current_food[i][j]:
                    #Then compute manhattan distance from state to that food
                    new_man = self.manhattan_distance((x,y),(i,j))
                    #If new distance is bigger than previous maximum one, update
                    if new_man > max_man:
                        max_man = new_man
        return max_man
    
    def manhattan_sum(self, state):
        """
        Given a pacman state, computes the sum of all manhattan distances between
        that state and all the leftover foods.
        Arguments:
        ----------
        - `state`: the current game state.
        Return:
        -------
        - The sum of all manhattan distances from the current state to all the left foods.
        """
        sum_man = 0
        x, y = state.getPacmanPosition()
        current_food = state.getFood()

        #For each position check if there is food or not
        for i in range(current_food.width):
            for j in range(current_food.height):
                if current_food[i][j]:
                    #Then compute manhattan distance from state to that food
                    new_man = self.manhattan_distance((x,y),(i,j))
                    #Add that distance to the sum
                    sum_man += new_man
        return sum_man
    
    def construct_path(self, state, meta):
        """ 
        Given a pacman state and a dictionnary, produces a backtrace of the actions 
        taken to find the food dot, using the recorded meta dictionary.
        Arguments:
        ----------
        - `state`: the current game state. 
        - `meta`: a dictionnary containing the path information from one node to another.
        Return:
        -------
        - A list of legal moves as defined in `game.Directions`
        """     
        action_list = list()
        
        # Continue until you reach root meta data (i.e. (None, None))
        while meta[state][0] is not None:
            state, action = meta[state]
            action_list.append(action)

        return action_list
    
    def compute_tree(self, state, heuristic):
        """
        Given a pacman state and a heuristic function, computes a path from that 
        state to a state where pacman has eaten all the food dots.
        Arguments:
        ----------
        - `state`: the current game state.
        Return:
        -------
        - A list of legal moves as defined in `game.Directions`
        """
        fringe = PriorityQueue() # a priority queue
        visited = set() # an empty set to maintain visited nodes

        # a dictionary to maintain path information : key -> (parent state, action to reach child)
        meta = dict()
        meta[state] = (None, None)

        #Append root
        fringe.update(state,1)

        # While not empty
        while not fringe.isEmpty(): 
            #Pick one available state
            current_cost, current_node = fringe.pop()

            if current_node.isWin():
                return self.construct_path(current_node, meta)

            #For each successor of the current node
            for next_node, next_action in current_node.generatePacmanSuccessors():
                #Check if it was already visited
                if hash((next_node.getPacmanPosition(), next_node.getFood())) not in visited:
                    #Successor wasn't visisted, we enfringe it
                    meta[next_node] = (current_node, next_action) 
                    
                    #Assign priority based on the presence of food
                    x,y = next_node.getPacmanPosition()
                    cost = 0 if current_node.hasFood(x,y) else 1
                    new_cost = current_cost + cost

                    #Assign priority f(n) = g(n) + h(n) and update node
                    priority = new_cost + heuristic(current_node)
                    fringe.update(next_node, priority)

            #Add the current node to the visited set
            visited.add(hash((current_node.getPacmanPosition(), current_node.getFood())))

    def get_action(self, state):
        """
        Given a pacman game state, returns a legal move.
        Arguments:
        ----------
        - `state`: the current game state.
        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """
        if not self.nextactions:
            self.nextactions = self.compute_tree(state,self.manhattan_sum)

        return self.nextactions.pop()