#!/usr/bin/python           # This is server.py file

import socket  # Import socket module
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os

INFINITY = 1000000

def receive(socket):
    msg = ''.encode()  # type: str

    try:
        data = socket.recv(1024)  # type: object
        msg += data
    except:
        pass
    return msg.decode()


def send(socket, msg):
    socket.sendall(msg.encode())


def empty_board(board):
    if sum(board[:6]) == 0 or sum(board[7:13]) == 0:
        return True
    else:
        return False
    
    
def make_move(board, move):
    if move in range(0,6):
        skip = 13
        box = 6
        moves = range(0,6)
    else:
        skip = 6
        box = 13
        moves = range(7,13)
       
    result = board[0:]
    result[move] = 0
    last = move + board[move]
    
    # the player deposits one of the stones in each hole until the stones run out
    for i in range(move + 1, last+1):
        if i != skip:
            result[i%14] += 1
        else:
            if skip == 6:
                result[7] += 1
            else:
                result[0] += 1
                
    # If the last piece you drop is in an empty hole on your side, you capture that piece and any pieces in the hole directly opposite.         
    if result[last%14] == 1:
        if last%14 in moves:    # check if the hole on your side
            result[last%14] = 0
            result[box] += 1            
            index_opposite = last%14 + (12 - (last%14)*2)
            result[box] += result[index_opposite]
            result[index_opposite] = 0
    return result


def side_sum(board, pturn):
    result = 0
    if pturn==1:
        for x in range(0,6):
            if x in [4,5]:
                result+= board[x]*1
            if x in [1,2,3]:
                result+= board[x]*0.9
            if x == 0:
                result+= board[x]*0.7

    else:
        for x in range(7,13):
            if x in [11,12]:
                result+= board[x]*1
            if x in [8,9,10]:
                result+= board[x]*0.9
            if x == 7:
                result+= board[x]*0.7
    return int(result)


def opposite_potential(board, pturn):
    opposite = 0
    for x in range((pturn-1)*7, (pturn-1)*7+6):
        last = (board[x] + x) % 13
        if board[x] != 0 and board[last] == 0 and last >= (pturn-1)*7 and last < (pturn-1)*7+6:
            if board[(12 - last)] > opposite:
                opposite = board[(12 - last)]
    return opposite


def utility(board, pturn, empty, depth):
    opposite = opposite_potential(board.copy(), pturn)     # potentially possible stealing stones
    if pturn == 1:
        if board[6] > 24 or (sum(board[:7]) > sum(board[7:]) and empty):
            return 1000 + depth
        elif board[13] > 24 or (sum(board[:7]) < sum(board[7:]) and empty):
            return -1000 - depth  
        else:
            return board[6] - board[13] + side_sum(board, True) - side_sum(board, False) + opposite
                
     
    else:
        if board[13] > 24 or (sum(board[:7]) < sum(board[7:]) and empty):
            return 1000 + depth
        elif board[6] > 24 or (sum(board[:7]) > sum(board[7:]) and empty):
            return -1000 - depth          
        
        else:
            return board[13] - board[6] + side_sum(board, False) - side_sum(board, True) + opposite        

def free_turn(board,pturn,move):
    if pturn==1:
        return (board[move]+move)%14 == 6
    else:
        return (board[move]+move)%14 == 13


def minmax(board, depth, pturn, isMax, alpha, beta):
    
    if pturn==1:
        if board == [4,4,4,4,4,4,0,4,4,4,4,4,4,0]:
            return [-1000, 3]
        if board == [4,4,0,5,5,5,1,4,4,4,4,4,4,0]:
            return [-1000, 6]       
    else:
        if board == [4,4,4,4,4,4,0,4,4,4,4,4,4,0]:
            return [1000, 10]
        if board == [4,4,4,4,4,4,0,4,4,0,5,5,5,1]:
            return [1000, 8]        
        
    if depth == 3 or empty_board(board):
        empty = empty_board(board)
        return [utility(board, pturn, empty, depth), None]
            
    if isMax:        
        maxVal = -INFINITY
        optMove = 0
        for i in range((pturn-1)*7, (pturn-1)*7+6):
            if board[i] == 0:
                continue
            if free_turn(board,pturn,i):
                current_val = minmax(make_move(board, i), depth + 1,  pturn, True, alpha, beta)[0]
            else:
                current_val = minmax(make_move(board, i), depth + 1, pturn, False, alpha, beta)[0]
            if current_val > maxVal:
                maxVal = current_val
                optMove = str(i+1)
            alpha = max(alpha, maxVal)
            if beta <= alpha:
                break            
        return [maxVal, optMove]

    else:
        minVal = INFINITY
        optMove = 0
        for i in range((pturn-1)*7, (pturn-1)*7+6):
            if board[i] == 0:
                continue
            if free_turn(board,pturn,i):
                current_val = minmax(make_move(board, i), depth + 1, pturn, False, alpha, beta)[0]
            else:
                current_val = minmax(make_move(board, i), depth + 1, pturn, True, alpha, beta)[0]
            if current_val < minVal:
                minVal = current_val
                optMove = str(i+1)
            beta = min(beta, minVal)
            if beta <= alpha:
                break                
        return [minVal, optMove]


def print_board(board):
    print(board[13], end='\t')
    for val in board[12:6:-1]:
        print(val, end=' ')
    print('')
    print(' ', end='\t')
    for val in board[:6]:
        print(val, end=' ')
    print('\t', board[6])
    print('')


# VARIABLES
playerName = 'Yaroslav Hrytsenko'
host = '127.0.0.1'
port = 30000  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
pool = ThreadPool(processes=1)
gameEnd = False
MAX_RESPONSE_TIME = 5

print('The player: ' + playerName + ' starts!')
s.connect((host, port))
print('The player: ' + playerName + ' connected!')

iteration = 0

while not gameEnd:
    asyncResult = pool.apply_async(receive, (s,))
    startTime = time.time()
    currentTime = 0
    received = 0
    data = []
    while received == 0 and currentTime < MAX_RESPONSE_TIME:
        if asyncResult.ready():
            data = asyncResult.get()
            received = 1
        currentTime = time.time() - startTime

    if received == 0:
        print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
        gameEnd = 1

    if data == 'N':
        send(s, playerName)

    if data == 'E':
        gameEnd = 1

    if len(data) > 1:

        # Read the board and player turn
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        playerTurn = int(data[0])
        i = 0
        j = 1
        while i <= 13:
            board[i] = int(data[j]) * 10 + int(data[j + 1])
            i += 1
            j += 2
            
        ################
        print_board(board)
        move = str(minmax(board, 0, playerTurn, True, -INFINITY, +INFINITY)[1])
        iteration += 1
        print("Iteration", iteration, "move", move)
        ################
        send(s, move)