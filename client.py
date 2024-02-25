# Abby Peterson, 02/21/24
# Othello remote player for Atomic Object JAR game board

import sys # for python runtime env
import json # to work with the JSON data (sent to server)
import socket # for the network (bc this is part of a client/server application)

def add_valid_spot(all_options, found_opt):
  '''
  GIVEN: master options list we are adding to when searching this boards opts
  PURPOSE: add current spot we found in check_line() to master dict if it's valid
  '''
  cur_key = found_opt[1] #spot
  cur_val = found_opt[0] #pts found from that one search
  #TEST print('results for that spot {!r} - pts:{!r}'.format(cur_key, cur_val)) 
  if cur_val > 0: #this is a space we can play on
    all_options.setdefault(cur_key, 0) #if spot is already an option, this line does nothing
    all_options[cur_key] += cur_val #sum up points related to playing in that spot (may be adding to 0)

def check_line(board, rel_loc, start_spot, player, opp, all_opts):
  '''
  PURPOSE: Looks at the corresponding row/col/diag of the cur empty adj spot to see/return possible points if played there
    If spot is: a corner-look at the mirrored & extending diag, vertical-look at that column (down/up depending), horizontal-look at that row (R/L depending)
  GIVEN: board, adjactent (start) spot and location relative to opp piece found, which players we vs the opponent are
  RETURNS: None, calls funct to add to all_opt dictionary so we can collect all options before choosing which to play in get_move()
  '''
  #TEST print('Checking row/col/diag') 
  # Initialize needed variables
  pts = 0
  pos_pts = 0 # possible points when searching along cur row/col/diag
  spot = [-1,-1]
  r_increment = -1*rel_loc[0] # set depending on type of line we are searching
  c_increment = -1*rel_loc[1] # set depending on type of line we are searching
  r = start_spot[0]
  c = start_spot[1]
  
  # Checking line loop... spot[r,c] changes as we look WHILE r & c are in range of the board grid
  r+=r_increment
  c+=c_increment
  while (r >= 0 and r < 8 and c >= 0 and c < 8):
    #TEST print('Looking at [{!r},{!r}]'.format(r,c)) 
    spot = board[r][c]
    if spot == opp: pos_pts+=1 #possible piece we can turn
    else:
      if spot == player: #valid row play! but counting stops
        pts=pos_pts
        #TEST print('my own spot at [{!r},{!r}] so future opts don\'t matter. PTS: {!r}'.format(r,c,pts)) 
      #else: #TEST print('empty spot at [{!r},{!r}] stops opts. PTS: {!r}'.format(r,c,pts)) 
      break
    r+=r_increment #new
    c+=c_increment #new
  add_valid_spot(all_opts, (pts, (start_spot[0],start_spot[1])))
  
def search_adjacents(board, row, col, player, opp, all_options):
  # Loop through surrounding spots to see open potential spots, careful of edge of board
  for dr in range(-1 if (row > 0) else 0 , 2 if (row < 7) else 1):
    for dc in range(-1 if (col > 0) else 0,2 if (col < 7) else 1):
      cur_r = row+dr
      cur_c = col+dc
      cur_spot = board[cur_r][cur_c]
      if cur_spot == 0: # found empty spot adjacent to opp
        #TEST print('found empty spot adjacent to opp at [{!r},{!r}]'.format(cur_r,cur_c))  
        check_line(board, (dr, dc), (cur_r, cur_c), player, opp, all_options)
        #TEST print('results for that empty spot - pts:{!r}, best_spot{!r}'.format(pts, best_spot))

def get_move(player, board):
  '''
  GIVEN: player: 1 or 2, board: list of game board rows (8x8) -- 0 empty, 1 p-1 spot, 2 p-2 spot
  RETURN: players calculated spot for next play to send -- must be valid option (add brains L8R)
  '''
  opp = 1 # opponents player #
  if player == 1: opp = 2
  all_options = {} #key: spot, value: points - dict fixes issue of summing up overlapping spots! (used to be a list)

  # Determine valid moves...
  # Loop through grid board # TODO simplify loop bc rn spots will overlap/options will be redundant
  for r in range(8):
    for c in range(8):
      # if found an opponents piece, check adjacent spot where I can potentially play
      if board[r][c] == opp:
        #TEST print('found opponents piece at [{!r},{!r}]'.format(r,c))  
        search_adjacents(board, r, c, player, opp, all_options) #cur_options: [[pts, spot]]
  
  # TODO determine best move
  best_opt = (-1,-1) #default invalid
  #TEST print('Found options: {!r}'.format(all_options)) 
  if len(all_options) != 0: # just incase
    best_opt = max(all_options, key=all_options.get) #returns the key (spot) in this dict that has the highest value (pts)
  #TEST print('Best Opt: {!r}'.format(best_opt)) 
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
