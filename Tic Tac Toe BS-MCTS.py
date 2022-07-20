#Implementation of Two Player Tic-Tac-Toe game in Python.


import math
import random
import numpy as np
from collections import defaultdict
import copy



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
            root_node = BSMCTSNode(root_node = True, color = 'O', beliefState = [Belief(x, 1)])
            actions, weights = BSMCTS(root_node, 1, 100)
            move = actions[np.argmax(weights)]
            
        if move in x.get_legal_moves():
            x.move(move)
            
            if x.game_result() != None:
                print("Game Result: " + x.game_result())
                x.printBoard()
                break
        else:
            print("INVALID MOVE")
        
        
          



        
    
    
    

class BSMCTSNode():
    def __init__(self, beliefs = [], parent=None, parent_action=None, root_node = False, color = None, beliefState = [], playerColor = None):
        self.beliefs  = beliefs
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.visits = 0
        self.reward = 0
        self.root_node = root_node
        self.color = color
        
        self.beliefState = beliefState
        
        self.playerColor = playerColor
        
        self.actions = []
        
        if self.root_node:
            self.playerColor = self.color
        
    
    
    def get_visits(self):
        return self.visits
    
    def get_reward(self):
        return self.reward
    
    def generateBelief(self):
        belief = random.sample(self.beliefState, 1)[0]
        
        if belief not in self.beliefs:
            for action in belief.get_legal_actions(belief.board):
                if action not in self.actions:
                    self.actions.append(action) 
        #print(belief)
        return belief
    
    def isPlayerNode(self):
        return self.color == self.playerColor
  

def nodeTakeAction(node, action):
    if node.color == 'X':
        new_color = 'O'
    else:
        new_color = 'X'
    
    new_beliefs = []
    
    for belief in node.beliefs:
        new_state = copy.deepcopy(belief.board)
        
        if action in new_state.get_legal_moves():
            new_state.move(action)
            new_beliefs.append(Belief(new_state, belief.probability))

    return BSMCTSNode(new_beliefs, node, action, False, new_color, node.playerColor)


def maxRewardAction(node, backup = False):
    choices_weights = []
    for action in node.actions:
        reward = actionReward(node, action)

        choices_weights.append(reward)
    print(node.actions)
    print(choices_weights)
    
    if backup:
        return node.actions, choices_weights
    else:
        return node.actions[np.argmax(choices_weights)]

def actionVisits(node, action):
    visits = 0
    for belief in node.beliefs:
        if action in belief.actionVisits.keys():
            visits += belief.actionVisits[action]
        
    return visits


def actionReward(node, action):
    reward = 0
    for belief in node.beliefs:
        if action in belief.actionRewards.keys():
            reward += belief.actionRewards[action]
        
    return reward
         

"""
Broot , maximal samplings T, maximal iterations S
1: function BS-MCTS Broot
2: t ← 1
3: repeat
4: γ ← Sampling(Broot)
5: s ← 1
6: repeat
7: R ← Search(γ,Broot)
8: N(γ) ← N(γ) + 1
9: s ← s + 1
10: until s > S
11: t ← t + 1
12: until t > T
13: return a ← argmaxa∈A(Br o o t )U(Broot, a)
14: end function

"""
def BSMCTS(root_node, max_samples, max_iterations):
    t = 1
    while (t <= max_samples):
        belief = sampling(root_node)
        s = 1
        
        while (s <= max_iterations):
            reward = search(belief, root_node)
            belief.visits += 1
            s += 1
        
        t += 1
    
    
    actions, weights = maxRewardAction(root_node, backup = True)
    
    return actions, weights
    

"""

15: function Expansion γ, B
16: N(γ) ← 0
17: for all a ∈ A(γ) do
18: if B · a not in the tree then
19: add B · a to the tree
20: end if
21: if γ · a not in B · a then
22: add γ · a to B · a
23: N(γ, a) ← 0
24: U(γ, a) ← 0
25: end if
26: end for
27: end function
"""

def expansion(belief, node):
    
    
    for action in belief.actions():
        
        if action not in [c.parent_action for c in node.children]:
            new_node = nodeTakeAction(node, action)
            node.children.append(new_node)
            
        else:
            for c in node.children:
                if c.parent_action == action:
                    action_node = c
                    break
                
            new_belief = beliefTakeAction(belief, action)
            if new_belief not in action_node.beliefs:
                action_node.beliefs.append(new_belief)
            

"""

28: function SamplingBroot
29: generate new γ
30: add γ to Broot
31: end function
"""            

def sampling(root_node):
    belief = root_node.generateBelief()
    #print(belief)
    root_node.beliefs.append(belief)
    return belief
    
"""

32: function Search γ,B
33: if N(B) = 0 then
34: R ← Simulation(γ)
35: return R
36: end if
37: if γ has no children then
38: Expansion(γ,B)
39: end if
40: N(γ) ← N(γ) + 1
41: action a← Selection(γ,B)
42: R←−Search(γ · a,B · a)
43: N(γ, a) ← N(γ, a) + 1
44: U(γ, a) ← U(γ, a) + 1
N (γ ,a) [R − U(γ, a)]
45: return R
46: end function

"""

def search(belief, node):
    #print(str(belief))
    if (node.visits == 0):
        node.visits += 1
        reward = belief.simulate()
        return reward
    
    if (node.children == []):
        if not belief.is_game_over(belief.board):
            expansion(belief, node)
        else:
            return belief.game_result(belief.board, node.color)
            
    node.visits += 1    
    belief.visits += 1
    action = selection(belief, node)
    
    for c in node.children:
        if c.parent_action == action:
            node_to_search = c
            break
    
    reward = -1 * search(beliefTakeAction(belief, action), node_to_search)
    
    if action in belief.actionVisits.keys():
        belief.actionVisits[action] += 1
    else:
        belief.actionVisits[action] = 1
    
    #Iterative Backpropogation
    if action in belief.actionRewards.keys():
        belief.actionRewards[action] += (1/belief.actionVisits[action]) * (reward - belief.actionRewards[action])
    else:
        belief.actionRewards[action] = reward
    #print(belief.actionRewards[action])
    return reward

"""
47: function Selectionγ, B
48: if B is Player node then
49: a ← argmaxa∈A(γ )VplayerNode (B, a)
50: else
51: a ← RouletteWheelSelection(Pro(ai))
52: end if
53: return a
54: end function
"""

def selection(belief, node):
    
    if node.isPlayerNode():
        action = maxNodeRewardEstimation(node,belief)
        
    else:
        action = roulette_wheel_selection(get_action_scores(node))
        
    return action

def maxNodeRewardEstimation(node, belief):
    choices_weights = []
    actions = belief.actions()
    for action in actions:
        if action in belief.actionVisits.keys():
            reward = nodeRewardEstimation(node, action)
        else:
            reward = 0

        choices_weights.append(reward)
   
    return actions[np.argmax(choices_weights)]

def nodeRewardEstimation(node,action):
    exploration = 0.7
    U = actionReward(node,action) 
    lnN = math.log(node.visits)
    NBa = actionVisits(node, action)
    return U + exploration * math.sqrt(lnN / NBa)



def get_action_scores(node):
    
    action_scores = []
    for c in node.children:
        action = c.parent_action
        U = actionReward(node,action)
        lambada = 0.7
        score = math.exp(U * lambada)
        
        action_scores.append([action, score])
        
    return action_scores
        

def roulette_wheel_selection(actions):
    maximum = sum(action[1] for action in actions)
    pick = random.uniform(0, maximum)
    current = 0
    for action in actions:
        current += action[1]
        if current > pick:
            return action[0]
    
class Belief():
    
    def __init__(self, board, probability):
       self.visits = 0
       self.reward = 0
       self.board = board
       self.probability = probability
       self.actionVisits = {}
       self.actionRewards = {}
       
      
    def __repr__(self):
        info = " Belief - Board: " + self.board.getStr() + " probability: " + str(self.probability) + " visits: " + str(self.actionVisits) + " reward: " + str(self.actionRewards)
        return info
    
    
    
    def simulate(self):
        
        board = self.board
        new_board = copy.deepcopy(board)
        
        while self.is_game_over(new_board) == False:
            moves = self.get_legal_actions(new_board)
            move = random.choice(moves)
            new_board = self.move(new_board, move)
            
        return self.game_result(new_board, board.turn)

 
    
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

    def actions(self):
        return self.get_legal_actions(self.board)  

def beliefTakeAction(belief, action):
    new_state = copy.deepcopy(belief.board)
    new_state.move(action)
    
    return Belief(new_state, belief.probability)
      

  
    
    
    
game()