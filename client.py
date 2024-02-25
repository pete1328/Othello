#!/usr/bin/python

# Abby Peterson, 02/21/24
# Othello remote player for Atomic Object JAR game board

#2/22 NOTES ...
# both remote, p2 "always" wins (4 tries so far)
# against random (games so far)
#   p1 remote won
#   p2 remote lost
#   p2 remote won
#   p1 remote TIE
#   p1 remote won
#2/24 NOTES...
# both remote, p1 wins (4 tries so far)
# p1 remote lost, won, lost
# p2 remote lost, won, won
#2/25 NOTES...
# p2 remote won, TIE, TIE, lost, lost
# p1 remote won, lost, lost, won, lost

import sys
import json
import socket

def check_line(board, rel_loc, start_spot, player, opp):
  print('Checking row/col/diag')
  pts = 0
  pos_pts = 0 # possible points when searching along cur row/col/diag
  spot = [-1,-1]
  valid = 0
  # if cur_spot is a corner -- look at the mirrored & extending diag
  # elif cur_spot is vertical -- look at that column (down or up depending)
  # elif cur_spot is horizontal -- look at that row (go R or L depending)
  r_increment = -1*rel_loc[0] # set depending on type of line we are searching
  c_increment = -1*rel_loc[1] # set depending on type of line we are searching

  # Checking line loop... spot[r,c] changings as we look WHILE r & c <= 7
  r = start_spot[0]
  c = start_spot[1]
  #old - while ((r < 7 if (r_increment > 0) else r > 0) and (c < 7 if (c_increment >= 0) else c > 0)):
  r+=r_increment
  c+=c_increment
  while (r >= 0 and r < 8 and c >= 0 and c < 8):
    #old - r+=r_increment
    #old - c+=c_increment
    print('Looking at [{!r},{!r}]'.format(r,c))
    spot = board[r][c]
    if spot == opp: pos_pts+=1
    elif spot == player:
      pts=pos_pts
      print('my own spot at [{!r},{!r}] so future opts don\'t matter. PTS: {!r}'.format(r,c,pts))
      return (pts, (start_spot[0],start_spot[1]))
    else:
      print('empty spot at [{!r},{!r}] stops opts. PTS: {!r}'.format(r,c,pts))
      return (pts, (start_spot[0],start_spot[1])) #an empty spot
    r+=r_increment #new
    c+=c_increment #new
  return (pts, (start_spot[0],start_spot[1]))
  
def search_adjacents(board, row, col, player, opp):
  options = [] #list of all found playable spots w/corresponding pts that would turn
  # Loop through surrounding spots to see open potential spots, careful of edge of board
  for dr in range(-1 if (row > 0) else 0 , 2 if (row < 7) else 1):
    for dc in range(-1 if (col > 0) else 0,2 if (col < 7) else 1):
      cur_r = row+dr
      cur_c = col+dc
      cur_spot = board[cur_r][cur_c]
      if cur_spot == 0:
        print('found empty spot adjacent to opp at [{!r},{!r}]'.format(cur_r,cur_c))
        pts, best_spot = check_line(board, (dr, dc), (cur_r, cur_c), player, opp)
        print('results for that empty spot - pts:{!r}, best_spot{!r}'.format(pts, best_spot))
        if pts != 0:
          print('adding {!r} as an option'.format(best_spot))
          options.append([pts, best_spot])
  return options

def get_move(player, board):
  '''
  GIVEN: player: 1 or 2, board: list of game board rows (8x8) -- 0 empty, 1 p-1 spot, 2 p-2 spot
  RETURN: players calculated spot for next play to send -- must be valid option (add brains L8R)
  '''
  opp = 1 # opponents player #
  if player == 1: opp = 2
  all_options = {} #key: spot, value: points
  # Determine valid moves...
  # Loop through grid board # TODO simplify loop bc rn spots will overlap/options will be redundant
  for r in range(8):
    for c in range(8):
      # if found an opponents piece, see if I could place any piece to turn it
      if board[r][c] == opp:
        print('found opponents piece at [{!r},{!r}]'.format(r,c)) #CHECK 
        cur_options = search_adjacents(board, r, c, player, opp) #cur_options: [[pts, spot]]
        for opt in cur_options:
          #OLD - all_options.append(opt)
          # Dict fixes issue of summing up overlapping spots! (used to be list)
          cur_key = opt[1] #spot
          cur_val = opt[0] #pts found from that one search
          all_options.setdefault(cur_key, 0) #if spot is already an option, this line does nothing
          all_options[cur_key] += cur_val #sum up points related to playing in that spot (may be adding to 0)
          # if cur_key in all_options: OLD
          #   all_options[cur_key] += cur_val
          # else: all_options[cur_key] = cur_val

  # TODO determine best move
  best_opt = (-1,-1) #default TODO what to send to pass the turn
  print('Found options: {!r}'.format(all_options))
  if len(all_options) != 0:
    best_opt = max(all_options, key=all_options.get)
  print('Best Opt: {!r}'.format(best_opt)) #returns the key (spot) in this dict that has the highest value (pts)
  return [best_opt[0],best_opt[1]] #formatting to a list for sending


def prepare_response(move):
  '''
  GIVEN: list of len 2 (x,y) for players next move
  RETURN: reformatted move as a JSON array to send as response
  '''
  response = '{}\n'.format(move).encode() # return it as a JSON array, followed by a newline, Ex: `"[1,2]\n"`
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337 # defining port num (for client server to connect)
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname() # defining local host port num

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initializing socket for connection
  try:
    sock.connect((host, port)) 
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8'))) # Ex. `{"board":<[8x8]>,"maxTurnTime":15000,"player":1}\n`
      board = json_data['board'] # Ex.[[0,0,0,0,0,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,0,2,0,0,0],[0,0,0,1,2,0,0,0],[0,0,0,1,2,2,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player'] # can be set in terminal command, but never assume val
      print(player, maxTurnTime, board)

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close() # ends the connection
