from random import randint
from BoardClasses import Move
from BoardClasses import Board
import sys
from copy import deepcopy
import time
from collections import defaultdict
import math
### TO REMOVE ###
import os
#################

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

# Variables Available:
# Board:
# col: The number of columns.
# row: The number of rows.
# p: Number of rows filled with Checker pieces at the start.

# Move:
# l: list describing the move

# Checkers:
# color: color of the checker piece.
# location: a tuple describing the location of the checker piece


# Functions Available:
# Board:
# show_board: Prints out the current board to the console
# get_all_possible_moves: Returns all moves possible in the current state of the board
# is_win: Check if there is a winner. Return which player wins.

# Move:
# from_str: Makes a move object from a str describing the move.

# Checkers:
# get_color: Returns the color of this piece.
# get_location: Returns the location of this piece.
# get_possible_moves: Returns all moves possible for this checker piece in the current state of the board

# White pieces are studentAI (positive)
# Black pieces are opps (negative)

# cd into Tools, then: python3 AI_Runner.py 8 8 3 l ./Sample_AIs/Random_AI/main.py ../src/checkers-python/main.py
# DOES NOT WORK:
# python3 AI_Runner.py 8 8 3 l ../src/checkers-python/main.py ./Sample_AIs/Random_AI/main.py 
# 

# Player 1 is actually black and player 2 is white. The original is_win method is correct, and some of the code comments were wrong.


# 

# 12/4 TODO
# Expansion Issue
move_count = 0

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.opponent = {1:2, 2:1}
        self.color = 2 #init as white, 'W'
        self.count_white_kings = 0
        self.count_black_kings = 0
        

        self.MonteCarloTreeSearch = MonteCarloTreeSearch(Node(None, self.color, self.board, None, self.opponent))


        #TODO: REMOVE
        #DEBUG: write moves to file
        #TODO: remove
        # open('moves.txt', 'w').close()
        # self.fd = os.open("moves.txt", os.O_RDWR | os.O_CREAT)

        
    def get_move(self, move):
        global move_count
        
        if len(move) != 0: #given code
            self.updateBoard(move, self.opponent[self.color])
        else:
            #only time len(move) == 0 is if we are going first, black always goes first
            self.color = 1 #given code
            
            # Initialize MCTS
            self.MonteCarloTreeSearch.root = Node(None, self.color, self.board, None, self.opponent)
            
            # make a random first move
            move_count += 1


            randomFirstMove = self.MonteCarloTreeSearch.random_move(self.board, self.color) # self.color or self.opponent[self.color]?
            self.updateBoard(randomFirstMove, self.color)
            return randomFirstMove
        

        move_count += 1


        possible_moves = self.board.get_all_possible_moves(self.color)
        if len(possible_moves) == 1 and possible_moves[0]:
            self.updateBoard(possible_moves[0][0], self.color)
            return possible_moves[0][0]

        # Monte Carlo Tree Search
        single_move_time = 1
        if move_count <= 10:
            single_move_time = 6
        elif move_count <=25:
            single_move_time = 7
        elif move_count <= 50:
            single_move_time = 8
        else:
            single_move_time = 2
        
        bestMove = self.MonteCarloTreeSearch.search(single_move_time) # 3 for now
        self.updateBoard(bestMove, self.color)


        # update with time passed
        return bestMove

    # Double Check Unsure 
    def updateBoard(self, move, color):  

        self.board.make_move(move, color)

        for m,c in self.MonteCarloTreeSearch.root.children.items():
            if str(move) == str(m) and c != None:
                self.MonteCarloTreeSearch.root.parent = None
                self.MonteCarloTreeSearch.root = c
                return
            
        self.MonteCarloTreeSearch.root = Node(None, self.color, self.board, None, self.opponent)

    

    
    # def get_move(self,move):
    #     DEPTH = 4
    #     # isMaxPlayer = None
    #     if len(move) != 0:   # Not Our Move
    #         self.board.make_move(move,self.opponent[self.color]) #swap color if we have no moves
    #         # isMaxPlayer = True 
    #     else:                # Our Move
    #         self.color = 1 #swap color to 'B'
    #         # isMaxPlayer = False
    #     score, move = self.ab_pruning(move, DEPTH, -sys.maxsize, sys.maxsize, self.color)
    #     # score, move = self.minimax(move, DEPTH, self.color)
    #     self.board.make_move(move, self.color)

    #     self.move_count += 1

    #     return move
    

class Node():
    def __init__(self, parent, color, board, move, opponent):
        self.parent = parent
        self.color = color
        self.board = deepcopy(board)
        self.parent_win = 0
        self.opponent = opponent

        if move: 
            self.board.make_move(move, self.opponent[self.color])

        self.num_visits = 1
        self.ucb1 = 0
        self.wins = 0
        
        self.children = {}  # {move from paren : where move goes to}
        moves = self.board.get_all_possible_moves(self.color)

        # game not over yet, children should be populated with None
        if not self.board.is_win(self.opponent[self.color]):
            for r in range(len(moves)):
                for c in range(len(moves[r])):
                    self.children[moves[r][c]] = None
                

    def backpropagate(self, parent_win):
        '''
        Backpropagate until the root node, when no more parent, all nodes backpropagated and return 
        '''
        self.num_visits += 1

        if not self.parent:
            return
        else:
            self.parent.backpropagate(-1 * parent_win)
            
            if parent_win == 1:
                self.parent_win += 1
            elif parent_win == 0:
                self.parent_win += .75
            else:
                self.parent_win += 0.5

            self.ucb1 = (self.parent_win / self.num_visits) + (1.5 * math.sqrt(math.log(self.parent.num_visits) / self.num_visits))
            # + self.RAVE_bonus(self)
            # os.write(self.fd, f'evaluation_score = {self.piece_difference_score() + (0.5*self.current_king_score()) + (0.25*self.back_protectors_moved_score())}\n'.encode('utf-8'))
            # os.write(self.fd, f'self.ucb1 = {self.ucb1}\n'.encode('utf-8'))

    
    # def update_RAVE(self, node, selected_child):
    #     node.rave_visits += 1
    #     node.rave_total_score += selected_child.total_score

    # def RAVE_bonus(self,node):
    #     beta = 0.01  # Adjust as needed
    #     if node.rave_visits == 0:
    #         return 0
    #     return beta * math.sqrt(node.rave_visits / (3 * node.visits))
            



class MonteCarloTreeSearch(): 
    def __init__(self, root):
        self.root = root
        self.opponent = {1:2, 2:1}


        #FOR DEBUG
        # open('moves.txt', 'w').close()
        # self.fd = os.open("moves.txt", os.O_RDWR | os.O_CREAT)
          
    def search(self, search_time):
        # Searches the tree with MCTS until time is up

        time_limit = time.time() + search_time
        # os.write(self.fd, f'time_condition = {time.time() < time_limit}\n'.encode('utf-8'))
        while time.time() < time_limit:
            # expansion
            
            # os.write(self.fd, f'self.root = {self.root}\n'.encode('utf-8'))
            selected_node = self.expandNode(self.root)
            # os.write(self.fd, f'selected_node.children = {selected_node.children}\n'.encode('utf-8'))

            
            #simulate/rollout
            new_board = deepcopy(selected_node.board)
            new_board_color = selected_node.color
            win_value = new_board.is_win(self.opponent[new_board_color])
            
            
            parent_win = self.simulate_games(new_board, new_board_color, win_value) # passed new_board?

            
            # backpropagate
            if win_value == self.opponent[selected_node.color]:
                parent_win = 1
            elif win_value == selected_node.color:
                parent_win = -1
            else:
                parent_win = 0
            
            # if parent_win == None:
            #     print("Parent Win was not set properly")
        
            # update values in tree
            selected_node.backpropagate(parent_win)
    
        # os.write(self.fd, f'Right before Best move selection root.children = {self.root.children}\n'.encode('utf-8'))

        return self.selectBestMove()
    
    def random_move(self, board, color):
        #return a random move for this board and color
        moves = board.get_all_possible_moves(color)
        row_index = randint(0, len(moves) - 1)
        col_index = randint(0, len(moves[row_index]) - 1)
        return moves[row_index][col_index]

    

    def simulate_games(self, new_board, new_board_color, win_value):
        while win_value == 0: # 0 means still moves left
            #make the move
            move_to_make = self.random_move(new_board, new_board_color)
            new_board.make_move(move_to_make, new_board_color)

            #update win value
            win_value = new_board.is_win(new_board_color)

            #swap colors
            new_board_color = self.opponent[new_board_color]
        return win_value
    


    def expandNode(self, curNode):  
    # def expandNode(self, node):       
        '''
        Should populate the selected nodes list of children
        '''
        if not curNode.children:
            # os.write(self.fd, ("REACHED IF:\n" ).encode('utf-8'))
            return curNode
        elif None not in curNode.children.values():
            children = sorted(curNode.children.values(), key = lambda x: x.ucb1, reverse=True)
            # children.sort(key = lambda x: x.ucb1, reverse=True)
            return self.expandNode(children[0])
        else:
            for m,c in curNode.children.items():
                if c == None:
                    curNode.children[m] = Node(curNode, self.opponent[curNode.color], curNode.board, m, self.opponent)
                    return curNode.children[m]

        
        # os.write(self.fd, f'Node after expansion node.children = {node.children}\n'.encode('utf-8'))
        


    def selectBestMove(self):   


        if len(self.root.children.keys()) == 1: # forced moves get made instantly
            return list(self.root.children.keys())[0]
        
        # moveToChild is {move from parent (coord) : what node object that move points to}
        # moveToChild = {key: value for key, value in self.root.children.items() if value is not None}
        moveToChild = {key: value for key, value in self.root.children.items()}

        moveToChild = sorted(moveToChild.items(), key=lambda x : x[1].num_visits, reverse=True)

        return moveToChild[0][0]
    
    
    # Evaluation Heuristics
    def evaluate_board_score(self, board):
        '''
        returns an int evaluating the score of the board
        '''
        color_dict = {1: 'B', 2: 'W'}

        board_score = 0
        
        pieces_difference_score = self.piece_difference(board)
        current_king_score = self.count_kings(board)
        # back_protectors_moved_score = self.back_protectors_moved()
    
        board_score = pieces_difference_score + (0.5*current_king_score)
        
        return board_score
    
    def piece_difference(self, board):
        color_dict = {1: 'B', 2: 'W'}
        pieces_difference = 0
        if color_dict[self.color] == 'W':
            pieces_difference = board.white_count - board.black_count
        if color_dict[self.color] == 'B':
            pieces_difference = board.black_count - board.white_count
        return pieces_difference
        

    def count_kings(self, board):
        color_dict = {1: 'B', 2: 'W'}
        count_white_kings = count_black_kings = 0
        for row in board:
                for checker in row:
                    if checker.is_king and checker.color == 'B': # BLACK
                        count_black_kings += 1
                    if checker.is_king and checker.color == 'W': # WHITE
                        count_white_kings += 1
        if color_dict[self.color] == 'B':
            return count_black_kings - count_white_kings
        else:
            return count_white_kings - count_black_kings


    # TODO: Change to loop through top and bottom rows
    # def back_protectors_moved(self, board):
    #     color_dict = {1: 'B', 2: 'W'}
    #     board_protector_score = 0
    #     if (move_count <= 12):
    #         if color_dict[self.color] == 'B':
    #             if board[0][1] == '.':
    #                 board_protector_score -= 1
    #             if board[0][5] == '.':
    #                 board_protector_score -= 1
                
    #         if color_dict[self.color] == 'W':
    #             if board[7][2] == '.':
    #                     board_protector_score -= 1
    #             if board[7][6] == '.':
    #                     board_protector_score -= 1
    #     return board_protector_score












##### EVALUTATION SECTION ######
    # def evaluate_board_score(self):
    #     '''
    #     returns an int evaluating the score of the board
    #     TODO: Add adjustments to score for King pieces
    #     '''
    #     color_dict = {1: 'B', 2: 'W'}

    #     board_score = 0
        
    #     pieces_difference_score = self.piece_difference()
    #     current_king_score = self.count_kings()
    #     back_protectors_moved_score = self.back_protectors_moved()
    
    #     board_score = pieces_difference_score + (0.5*current_king_score) + (0.25*back_protectors_moved_score)
        
    #     return board_score
    
    # def piece_difference(self):
    #     color_dict = {1: 'B', 2: 'W'}
    #     pieces_difference = 0
    #     if color_dict[self.color] == 'W':
    #         pieces_difference = self.board.white_count - self.board.black_count
    #     if color_dict[self.color] == 'B':
    #         pieces_difference = self.board.black_count - self.board.white_count
    #     return pieces_difference
        

    # def count_kings(self):
    #     color_dict = {1: 'B', 2: 'W'}
    #     count_white_kings = count_black_kings = 0
    #     for row in self.board.board:
    #             for checker in row:
    #                 if checker.is_king and checker.color == 'B': # BLACK
    #                     count_black_kings += 1
    #                 if checker.is_king and checker.color == 'W': # WHITE
    #                     count_white_kings += 1
    #     if color_dict[self.color] == 'B':
    #         return count_black_kings - count_white_kings
    #     else:
    #         return count_white_kings - count_black_kings



    # def back_protectors_moved(self):
    #     color_dict = {1: 'B', 2: 'W'}
    #     board_protector_score = 0
    #     if (self.move_count <= 12):
    #         if color_dict[self.color] == 'B':
    #             if self.board.board[0][1] == '.':
    #                 board_protector_score -= 1
    #             if self.board.board[0][5] == '.':
    #                 board_protector_score -= 1
                
    #         if color_dict[self.color] == 'W':
    #             if self.board.board[7][2] == '.':
    #                     board_protector_score -= 1
    #             if self.board.board[7][6] == '.':
    #                     board_protector_score -= 1
    #     return board_protector_score

####### EVALUATION SECTION END ###########


######### MCTS SECTION START ###########

##### PSEUDOCODE #####

# class Node:
#   def __init__(self, m, p): # move is from parent to node
#     self.move, self.parent, self.children = m, p, []
#     self.wins, self.visits  = 0, 0

#   def expand_node(self, state):
#     if not terminal(state): # STUDENT COMMENT: we can use has no more moves left for this
#       for each non-isomorphic legal move m of state: ## WTF DOES THIS MEAN? I hope it just means for every legal move
#         nc = Node(m, self) # new child node # since its not a DFS, we might just have to use deepcopy
#         self.children.append(nc)

#   def update(self, r):
#     self.visits += 1
#     if r==win: #STUDENT COMMENT: use is_win == color for this one
#       self.wins += 1

#   def is_leaf(self):
#     return len(self.children)==0

#   def has_parent(self):
#     return self.parent is not None

# def mcts(state):
#   root_node  = Node(None, None)
#   while time remains: # STUDENT COMMENT: Time remains means depth for us
#     n, s = root_node, copy.deepcopy(state)
#     while not n.is_leaf():    # select leaf
#       n = tree_policy_child(n)
#       s.addmove(n.move)
#     n.expand_node(s)          # expand
#     n = tree_policy_child(n)
#     while not terminal(s):    # simulate
#       s = simulation_policy_child(s) # STUDENT COMMENT: also called rollout, gfg has this as random at first
#     result = evaluate(s) # STUDENT COMMENT: our heuristic goes here
#     while n.has_parent():     # propagate
#       n.update(result) #this loop can be kept nearly the same
#       n = n.parent

#     return best_move(tree)











####### AB PRUNING  ALGORITHM ########
    # def ab_pruning(self, move, depth, alpha, beta, passed_color_num):
    #     '''
    #     returns 2 Objects: Score of the most optimal move, the most optimal move
    #     '''
        

    #     if passed_color_num == self.color: isMaxPlayer = True
    #     else: isMaxPlayer = False
        
    #     color_dict = {1: 'B', 2: 'W'}
    #     # Base Case 
    #     if depth == 0 or self.board.get_all_possible_moves(color_dict[passed_color_num]) == 0: # 'B' or 'W'  
    #         score = self.evaluate_board_score()
    #         return score, move
    #         # return self.evaluate_board_score(passed_color_num), move
        
    #     nextMove = None
    #     if isMaxPlayer: 
    #         line = str.encode("MAXplayer reached, param number: " + str(passed_color_num) + ", color dict output: " + color_dict[passed_color_num] + "\n")
    #         os.write(self.fd, line)
    #         maxScore = -sys.maxsize
    #         for possible_moves in self.board.get_all_possible_moves(color_dict[self.color]):
    #             for move in possible_moves:
    #                 # turn 1 is B, 2 is W
    #                 # MAKE MOVE HERE
    #                 self.board.make_move(move, self.color)
    #                 line = str.encode("FROM MAXPLAYER MOVES LOOP, OPPONENT COLOR NUM: " + str(self.opponent[self.color]) + ", OPPONENT COLOR STR: " + color_dict[self.opponent[self.color]] + "\n")
    #                 os.write(self.fd, line)
    #                 curScore = self.ab_pruning(move, depth-1, alpha, beta, self.opponent[self.color])[0] 
    #                 #Subtree traversed, try next move
    #                 # self.board.undo()  # undos current leaf, then breaks out
                    
    #                 self.board.undo() 
                    
    #                 maxScore = max(maxScore, curScore)   # thinking move maxScore above undo, won't hurt runtime
    #                 if maxScore == curScore: 
    #                     nextMove = move
    #                 # Prune
    #                 alpha = max(alpha, maxScore)
    #                 if beta <= alpha:
    #                     break
    #         return maxScore, nextMove
                       
    #     else:
    #         # TODO: REMOVE
    #         line = str.encode("minplayer reached, param number: " + str(passed_color_num) + " color dict output: " + color_dict[passed_color_num] + "\n")
    #         os.write(self.fd, line)

    #         line = str.encode("minplayer reached, param number: " + str(passed_color_num) + ", GET ALL POSSIBLE OPPONENT COLOR PARAM: " + str(self.board.get_all_possible_moves(color_dict[self.opponent[self.color]])) + "\n")
    #         os.write(self.fd, line)

            
    #         minScore = sys.maxsize
    #         for possible_moves in self.board.get_all_possible_moves(color_dict[self.opponent[self.color]]):  # [Piece 1: [Move, Move, Move], Piece 2: [Move, Move, Move]]
    #             for move in possible_moves:
    #                 line = str.encode("FROM minplayer MOVES LOOP, OPPONENT COLOR NUM: " + str(self.opponent[self.color]) + ", OPPONENT COLOR STR: " + color_dict[self.opponent[self.color]] + "\n")
    #                 os.write(self.fd, line)
    #                 # MAKE MOVE HERE
    #                 self.board.make_move(move, self.opponent[self.color])
                    
    #                 curScore = self.ab_pruning(move, depth-1, alpha, beta, self.color)[0] # pass new board along

    #                 # Subtree Traversed, try the next move
    #                 self.board.undo()

    #                 minScore = min(minScore, curScore)
    #                 if minScore == curScore: 
    #                     nextMove = move
    #                 # Pruning
    #                 beta = min(beta, minScore)
    #                 if beta <= alpha:
    #                     break
                    
    #         return minScore, nextMove


####### AB PRUNING ALGORITHM END ############









