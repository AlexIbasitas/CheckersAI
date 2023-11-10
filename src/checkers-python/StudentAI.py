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

# python3 AI_Runner.py 8 8 3 l '~/CheckersAI/Tools/Sample_AIs/Random_AI/main.py' '~/CheckersAI/src/checkers-python/main.py'
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

        #TODO: REMOVE
        #DEBUG: write moves to file
            #TODO: remove
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
        score, move = self.minimax(move, DEPTH, self.color)
        
        self.board.make_move(move, self.color)
        return move
    
    # def get_move(self,move):
    #     if move.seq:
    #         # if move.seq is not an empty list
    #         self.board.make_move(move,self.opponent[self.color])
    #     else:
    #         self.color = 1
    #     moves = self.board.get_all_possible_moves(self.color)
    #     while True:
    #         try:
    #             for i,checker_moves in enumerate(moves):
    #                 print(i,':[',end="")
    #                 for j, move in enumerate(checker_moves):
    #                     print(j,":",move,end=", ")
    #                 print("]")
    #             index,inner_index = map(lambda x: int(x), input("Select Move {int} {int}: ").split()) # input is from console is handled here.
    #             res_move = moves[index][inner_index]
    #         except KeyboardInterrupt:
    #             raise KeyboardInterrupt
    #         except:
    #             print('invalid move')
    #             continue
    #         else:
    #             break
    #     self.board.make_move(res_move, self.color)
    #     return res_move
    
    

    
    def evaluate_board_score(self):
        '''
        returns an int evaluating the score of the board
        TODO: Add adjustments to score for King pieces
        '''
        color_dict = {1: 'B', 2: 'W'}

        for row in self.board.board:
            for checker in row:
                if checker.is_king and checker.color == 'B': # BLACK
                    self.count_black_kings += 1
                if checker.is_king and checker.color == 'W': # WHITE
                    self.count_white_kings += 1

        board_score = 0
        if color_dict[self.color] == 'W':
            board_score = self.board.white_count - self.board.black_count + ((0.5 * self.count_white_kings) - (0.5 * self.count_black_kings))
        if color_dict[self.color] == 'B':
            board_score = self.board.black_count - self.board.white_count + + ((0.5 * self.count_black_kings) - (0.5 * self.count_white_kings))
        self.count_white_kings = self.count_black_kings = 0
        return board_score

    def minimax(self, pos, depth, passed_color):
        '''
        returns 2 Objects: Score of the most optimal move, the most optimal move
        '''
       
        if passed_color == self.color: isMaxPlayer = True
        else: isMaxPlayer = False
        
        color_dict = {1: 'B', 2: 'W'}
        # Base Case 
        if depth == 0 or self.board.is_win(color_dict[passed_color]): # 'B' or 'W'
            #DEBUG: write moves to file
            #TODO: remove
            # line = str.encode(str(pos) + "\n")
            # os.write(self.fd, line)
            return self.evaluate_board_score(), pos
        
        nextMove = None
        if isMaxPlayer:
            maxScore = -sys.maxsize
            # get_all_possible_moves() returns [Move(), Move(), Move()]
            for possible_moves in self.board.get_all_possible_moves(color_dict[passed_color]):
                for move in possible_moves:
                    curScore = self.minimax(move, depth-1, self.color)[0] # current evaluation score only
                    maxScore = max(maxScore, curScore)
                    if maxScore == curScore: nextMove = move
            return maxScore, nextMove
                       
        else:
            minScore = sys.maxsize
            for possible_moves in self.board.get_all_possible_moves(color_dict[passed_color]):
                for move in possible_moves:
                    curScore = self.minimax(move, depth-1, self.opponent[self.color])[0]
                    minScore = min(minScore, curScore)
                    if minScore == curScore: nextMove = move

            return minScore, nextMove




class boardStateNode():
    eval_score = 0.0
    def __init__(self,board):
        # self.eval_score = evaluateBoard(board)
        pass
    
    def getEvalScore(self, board):
        return self.eval_score
        

class SearchTree():
    def __init__(self):
        root = boardStateNode(board) #pass it the initial board



# This is the initial get_move function, kept here for reference
# def get_random_move(self,move):
#     if len(move) != 0:
#         self.board.make_move(move,self.opponent[self.color])
#     else:
#         self.color = 1
#     moves = self.board.get_all_possible_moves(self.color)
#     index = randint(0,len(moves)-1)
#     inner_index =  randint(0,len(moves[index])-1)
#     move = moves[index][inner_index]
#     self.board.make_move(move,self.color)
#     return move