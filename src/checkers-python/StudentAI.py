from random import randint
from BoardClasses import Move
from BoardClasses import Board
import sys


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

# 

# python3 AI_Runner.py 8 8 3 l '~/CheckersAI/src/checkers-python/main.py' '~/CheckersAI/Tools/Sample_AIs/Random_AI/main.py' 

# 11/3 TODO
# Optimize the evaluation function to determine board score
# Add pruning
# 
# if type(turn) == int:
#  if turn == 1:
#     turn = 'B'
#  elif turn == 2:
#     turn = 'W'

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2, 2:1}
        self.color = 2 #init as white, 'W'
        self.count_white_kings = 0
        self.count_black_kings = 0


        self.move_count = 0
        #TODO: REMOVE
        #DEBUG: write moves to file
        #TODO: remove
        open('moves.txt', 'w').close()
        self.fd = os.open("moves.txt", os.O_RDWR | os.O_CREAT)

    def get_move(self,move):
        DEPTH = 4
        # isMaxPlayer = None
        if len(move) != 0:   # Not Our Move
            self.board.make_move(move,self.opponent[self.color]) #swap color if we have no moves
            # isMaxPlayer = True 
        else:                # Our Move
            self.color = 1 #swap color to 'B'
            # isMaxPlayer = False
        score, move = self.ab_pruning(move, DEPTH, -sys.maxsize, sys.maxsize, self.color)
        # score, move = self.minimax(move, DEPTH, self.color)
        self.board.make_move(move, self.color)

        self.move_count += 1

        return move
    

    

    
    def evaluate_board_score(self):
        '''
        returns an int evaluating the score of the board
        TODO: Add adjustments to score for King pieces
        '''
        color_dict = {1: 'B', 2: 'W'}

        board_score = 0
        
        pieces_difference_score = self.piece_difference()
        current_king_score = self.count_kings()
        back_protectors_moved_score = self.back_protectors_moved()
    
        board_score = pieces_difference_score + (0.5*current_king_score) + (0.25*back_protectors_moved_score)
        
        return board_score
    
    def piece_difference(self):
        color_dict = {1: 'B', 2: 'W'}
        pieces_difference = 0
        if color_dict[self.color] == 'W':
            pieces_difference = self.board.white_count - self.board.black_count
        if color_dict[self.color] == 'B':
            pieces_difference = self.board.black_count - self.board.white_count
        return pieces_difference
        

    def count_kings(self):
        color_dict = {1: 'B', 2: 'W'}
        count_white_kings = count_black_kings = 0
        for row in self.board.board:
                for checker in row:
                    if checker.is_king and checker.color == 'B': # BLACK
                        count_black_kings += 1
                    if checker.is_king and checker.color == 'W': # WHITE
                        count_white_kings += 1
        if color_dict[self.color] == 'B':
            return count_black_kings - count_white_kings
        else:
            return count_white_kings - count_black_kings



    def back_protectors_moved(self):
        color_dict = {1: 'B', 2: 'W'}
        board_protector_score = 0
        if (self.move_count <= 12):
            if color_dict[self.color] == 'B':
                if self.board.board[0][1] == '.':
                    board_protector_score -= 1
                if self.board.board[0][5] == '.':
                    board_protector_score -= 1
                
            if color_dict[self.color] == 'W':
                if self.board.board[7][2] == '.':
                        board_protector_score -= 1
                if self.board.board[7][6] == '.':
                        board_protector_score -= 1
        return board_protector_score

    def ab_pruning(self, move, depth, alpha, beta, passed_color_num):
        '''
        returns 2 Objects: Score of the most optimal move, the most optimal move
        '''
        

        if passed_color_num == self.color: isMaxPlayer = True
        else: isMaxPlayer = False
        
        color_dict = {1: 'B', 2: 'W'}
        # Base Case 
        if depth == 0 or self.board.get_all_possible_moves(color_dict[passed_color_num]) == 0: # 'B' or 'W'  
            score = self.evaluate_board_score()
            return score, move
            # return self.evaluate_board_score(passed_color_num), move
        
        nextMove = None
        if isMaxPlayer: 
            line = str.encode("MAXplayer reached, param number: " + str(passed_color_num) + ", color dict output: " + color_dict[passed_color_num] + "\n")
            os.write(self.fd, line)
            maxScore = -sys.maxsize
            for possible_moves in self.board.get_all_possible_moves(color_dict[self.color]):
                for move in possible_moves:
                    # turn 1 is B, 2 is W
                    # MAKE MOVE HERE
                    self.board.make_move(move, self.color)
                    line = str.encode("FROM MAXPLAYER MOVES LOOP, OPPONENT COLOR NUM: " + str(self.opponent[self.color]) + ", OPPONENT COLOR STR: " + color_dict[self.opponent[self.color]] + "\n")
                    os.write(self.fd, line)
                    curScore = self.ab_pruning(move, depth-1, alpha, beta, self.opponent[self.color])[0] 
                    #Subtree traversed, try next move
                    # self.board.undo()  # undos current leaf, then breaks out
                    
                    self.board.undo() 
                    
                    maxScore = max(maxScore, curScore)   # thinking move maxScore above undo, won't hurt runtime
                    if maxScore == curScore: 
                        nextMove = move
                    # Prune
                    alpha = max(alpha, maxScore)
                    if beta <= alpha:
                        break

                    
                    


            return maxScore, nextMove
                       
        else:
            # TODO: REMOVE
            line = str.encode("minplayer reached, param number: " + str(passed_color_num) + " color dict output: " + color_dict[passed_color_num] + "\n")
            os.write(self.fd, line)

            line = str.encode("minplayer reached, param number: " + str(passed_color_num) + ", GET ALL POSSIBLE OPPONENT COLOR PARAM: " + str(self.board.get_all_possible_moves(color_dict[self.opponent[self.color]])) + "\n")
            os.write(self.fd, line)

            
            minScore = sys.maxsize
            for possible_moves in self.board.get_all_possible_moves(color_dict[self.opponent[self.color]]):  # [Piece 1: [Move, Move, Move], Piece 2: [Move, Move, Move]]
                for move in possible_moves:
                    line = str.encode("FROM minplayer MOVES LOOP, OPPONENT COLOR NUM: " + str(self.opponent[self.color]) + ", OPPONENT COLOR STR: " + color_dict[self.opponent[self.color]] + "\n")
                    os.write(self.fd, line)
                    # MAKE MOVE HERE
                    self.board.make_move(move, self.opponent[self.color])
                    
                    curScore = self.ab_pruning(move, depth-1, alpha, beta, self.color)[0] # pass new board along

                    # Subtree Traversed, try the next move
                    self.board.undo()

                    minScore = min(minScore, curScore)
                    if minScore == curScore: 
                        nextMove = move
                    # Pruning
                    beta = min(beta, minScore)
                    if beta <= alpha:
                        break
                    
                   
                    

            return minScore, nextMove










# class Node:
#   def __init__(self, m, p): # move is from parent to node
#     self.move, self.parent, self.children = m, p, []
#     self.wins, self.visits  = 0, 0

#   def expand_node(self, state):
#     if not terminal(state): # STUDENT COMMENT: we can use has no more moves left for this
#       for each non-isomorphic legal move m of state:
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
#       s = simulation_policy_child(s)
#     result = evaluate(s) # STUDENT COMMENT: our heuristic goes here
#     while n.has_parent():     # propagate
#       n.update(result)
#       n = n.parent

#     return best_move(tree)
