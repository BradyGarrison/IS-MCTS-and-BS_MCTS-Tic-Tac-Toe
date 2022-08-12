#Implementation of Two Player Tic-Tac-Toe game in Python.


import math
import random
import numpy as np
from collections import defaultdict
import copy
from graphviz import Digraph
from anytree import NodeMixin, RenderTree
from anytree.exporter import DotExporter


class TreeNode(NodeMixin):
    def __init__(self, MovementMonteCarloTreeSearchNode, parent=None, name = None):
        self.children = [TreeNode(node, self, str(node.parent_action)) for node in MovementMonteCarloTreeSearchNode.children]
        self.visits = MovementMonteCarloTreeSearchNode._number_of_visits
        self.reward = MovementMonteCarloTreeSearchNode.reward
        self.color = MovementMonteCarloTreeSearchNode.state.turn
        try:
            self.selected_action = MovementMonteCarloTreeSearchNode.best_child().parent_action
        except:
            self.selected_action = None
        self.parent_action = MovementMonteCarloTreeSearchNode.parent_action
        self.parent = parent
        self.name = name
  

class tic_tac_toe_board():
    
    ''' We will make the board using dictionary 
        in which keys will be the location(i.e : top-left,mid-right,etc.)
        and initialliy it's values will be empty space and then after every move 
        we will change the value according to player's choice of move. '''

    def __init__(self, theBoard = {'7': ' ' , '8': ' ' , '9': ' ' ,
                '4': ' ' , '5': ' ' , '6': ' ' ,
                '1': ' ' , '2': ' ' , '3': ' ' }, turn = 'X', count = 0):
        self.theBoard = theBoard

        self.board_keys = []

        for key in self.theBoard:
            self.board_keys.append(key)
            
        self.turn = turn
        self.count = count
    
    ''' We will have to print the updated board after every move in the game and 
        thus we will make a function in which we'll define the printBoard function
        so that we can easily print the board everytime by calling this function. '''
    def printBoard(self):
        board = self.theBoard
        print(board['7'] + '|' + board['8'] + '|' + board['9'])
        print('-+-+-')
        print(board['4'] + '|' + board['5'] + '|' + board['6'])
        print('-+-+-')
        print(board['1'] + '|' + board['2'] + '|' + board['3'])
        
    def getStr(self):
        board = self.theBoard
        return board['1'] + board['2'] + board['3'] + board['4'] + board['5'] + board['6'] + board['7'] + board['8'] + board['9'] 


    def game_result(self):
        # Now we will check if player X or O has won,for every move after 5 moves. 
        
        theBoard = self.theBoard
        count = self.count
        
        
        if count >= 5:
            if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ': # across the top
                return self.turn
            elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ': # across the middle
                return self.turn
            elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ': # across the bottom
                return self.turn
            elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ': # down the left side
                return self.turn
            elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ': # down the middle
                return self.turn
            elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ': # down the right side
                return self.turn
            elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ': # diagonal
                return self.turn
            elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ': # diagonal
                return self.turn

        # If neither X nor O wins and the board is full, we'll declare the result as 'tie'.
        if count == 9:
            return "tie"

    def move(self, move):
        
        
        if self.theBoard[move] == ' ':
            self.theBoard[move] = self.turn
            self.count += 1
            self.board_keys.remove(move)
            
            if self.game_result() == None:
        
                if self.turn =='X':
                    self.turn = 'O'
                else:
                    self.turn = 'X'
                
    def get_legal_moves(self):
        return self.board_keys
    
            
def createTree():
    board = tic_tac_toe_board()
    root_node = MovementSOISMCTS([board], board.turn, True)
    test = TreeNode(root_node)

    for row in RenderTree(test):
        print("%s%s" % (row.pre, row.node.name))

    DotExporter(test,options = ["ratio = 1.5"], nodenamefunc = nodenamefunc, nodeattrfunc=nodeattrfunc, edgeattrfunc = edgeattrfunc).to_dotfile("ISMCTS v4.dot")
    


def nodenamefunc(node):
    return 'visits: %s, reward: %s' % (node.visits, node.reward)

def nodeattrfunc(node):
    if node.color == 'O':
        return "style=filled fillcolor=crimson shape=box"
    elif node.color == 'X':
        return "style=filled fillcolor=lightblue shape=circle"

def edgeattrfunc(node, child):
    
    if node.selected_action == child.parent_action:
        return 'color = purple label = %s' % child.parent_action
    
    return 'label = %s' % child.parent_action




# Now we'll write the main function which has all the gameplay functionality.
def game():

    x = tic_tac_toe_board()


    for i in range(10):
        x.printBoard()
        print("It's your turn," + x.turn + ".Move to which place?")
        print(x.get_legal_moves())
        
        if x.turn =='X':
            move = input()
        
        else:
            #move = input()
            move = MovementSOISMCTS([x], x.turn).parent_action
            
        if move in x.get_legal_moves():
            x.move(move)
            
            if x.game_result() != None:
                print("Game Result: " + x.game_result())
                x.printBoard()
                break
        else:
            print("INVALID MOVE")
        
        
          



        
    
    
    

def MovementSOISMCTS(board_set, color, returnNode = False):
    root = MovementMonteCarloTreeSearchNode(board_set = board_set, root_node = True, color = color)
    selected_nodes = root.best_action()
    
    if returnNode:
        return root
    
    return selected_nodes
        
    """
    make a tree
    (v,d) = select a node from starting state
    
    if there are still actions at this node:
        (v,d) = new node made by expanding current (v,d)
        
    get reward by simulating board
    backpropogate that reward
    
    return an action
        
    """       

    

class MovementMonteCarloTreeSearchNode():
    def __init__(self, state = None, parent=None, parent_action=None, root_node = False, board_set = None, color = None):
        self.state = state
        #print(self.state)
        self.board_set = board_set
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self.availability = 0 
        self._results = defaultdict(int)
        self.reward = 0
        self._untried_actions = {}
        self._actions = {}
        self.root_node = root_node
        self.color = color
        
        
        if not self.root_node:
            self._untried_actions = []
            self._untried_actions = self.untried_actions()
            self._actions = []
            self._actions = self.actions()
        
    
    
    def untried_actions(self):
        self._untried_actions = self.get_legal_actions(self.state)
        return self._untried_actions
    
    def actions(self):
        self._actions = self.get_legal_actions(self.state)
        return self._actions
    
    def get_visits(self):
        return self._number_of_visits
    
    
    def get_availability(self):
        return self.availability
    
    def get_reward(self):
        return self.reward
    
    
    def expand(self):
        if self.root_node:
            
            action = self._untried_actions[self.state.getStr()].pop(random.randint(0,len(self._untried_actions[self.state.getStr()])-1))
            #print(action)
            
            
        else:
            #print("Other node children: " + str(len(self.children)))
            action = self._untried_actions.pop(random.randint(0,len(self._untried_actions)-1))
            
        next_state = self.move(self.state, action)
        #print(next_state)
        child_node = MovementMonteCarloTreeSearchNode(state=next_state, parent=self, parent_action=action, color = self.color)
    
        self.children.append(child_node)
        return child_node
    
        """
        //expansion
        if v is nonterminal then
            choose at random an action a from node v that is compatible with d and does not exist in the tree
            add a child node to corresponding to the player 1 information set reached using action a
            and set it as the new current node v
        """
    
    
    def is_terminal_node(self):
        return self.is_game_over(self.state)
    
    
    def simulate(self):
        
        board = self.state
        new_board = copy.deepcopy(board)
        
        while self.is_game_over(new_board) == False:
            moves = self.get_legal_actions(new_board)
            move = random.choice(moves)
            new_board = self.move(new_board, move)
            
        return self.game_result(new_board, self.color)
    
    
        """
        //simulation
        run a simulation to the end of the game using determinization d
        """
    
    
    def backpropagate(self, result):
        self._number_of_visits += 1.
        self.reward += result
        if self.parent:
            self.parent.backpropagate(result)
            
            for child in self.parent.children:
                child.availability += 1
            
        """
        //backpropogation
        for each node visited during this iteration do
        
            update u’s visit count and total simulation reward
            
            for each sibling w of u that was available for
            selection when u was selected, including u itself do
                update w’s availability count
        """
    
    def is_fully_expanded(self):
        
        if self.root_node:
            return len(self._untried_actions[self.state.getStr()]) == 0
            
        else:
            return len(self._untried_actions) == 0
    
    
    def best_child(self, exploration=0.7, backup = False, printResult = False):
        #print("best child call")
        choices_weights = []
        for c in self.children:
            reward = c.get_reward()
            #print(reward)
            visits = c.get_visits()
            #print(visits)
            availability = c.get_availability()
            #choices_weights.append(reward / visits)
            choices_weights.append(reward / visits + exploration * math.sqrt(math.log(availability)/visits))
           # print(choices_weights)
        
        
        if printResult:
            #print(self.children[np.argmax(choices_weights)].parent_action, self.children[np.argpartition(choices_weights, -1)[-2]].parent_action)
            print([c.parent_action for c in self.children])
            print(choices_weights)
            #print(np.argmax(choices_weights))
        
        if backup:
            
            return self.children , choices_weights
            #return self.children[np.argmax(choices_weights)], self.children[np.argpartition(choices_weights, -1)[-2]]
        else:
            return self.children[np.argmax(choices_weights)]
    
    
    
    def select_and_expand(self):
        
        current_node = self
        #print(len(current_node.children))    
        while not current_node.is_terminal_node():
            
            if not current_node.is_fully_expanded():
                #print(self._untried_actions)
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node  
        
        """
        //Selection
        repeat
            descend the tree (restricted to nodes/actions compatible with d) using the chosen bandit algorithm 
            
        until a node is reached such that some action from v leads to a player 1 information set which is not currently in the tree
        
        or 
        
        until v is terminal
        """
    
   
    def best_action(self):
        exploration_number = 100
	
        for i in range(exploration_number):
            
            if self.root_node:
                #print(self.state)
                #print("")
                #if self.state == None or len(self._untried_actions[self.state.getStr()]) == 0:
                determinization = random.choice(self.board_set)
                #print("determinization: ")
                #print(determinization)
                #print("")
                self.state = determinization
                if self.state.getStr() not in self._untried_actions:
                    self._untried_actions[self.state.getStr()] = self.get_legal_actions(self.state)
                    self._actions[self.state.getStr()] = self.get_legal_actions(self.state)
                
            v = self.select_and_expand()
            #print("simulated board: ")
            #print(v.state)
            #print("")
            reward = v.simulate()
            #print(reward)
            v.backpropagate(reward)
	
        return self.best_child(backup=False, printResult = True)
    
    
    
    def get_legal_actions(self, board): 
        return board.get_legal_moves().copy()
        
    def is_game_over(self, board):
        
        result = board.game_result()
        
        if result == None:
            return False
        else:
            return True
        
    def game_result(self, board, color):
        
        
        result = board.game_result()
        
        if result == color:
            return +1
        elif result == "tie":
            return 0
        else:
            return -1
        
        
        
    def move(self, board,action):
        new_board = copy.deepcopy(board)
        new_board.move(action)
        return new_board
      
    
