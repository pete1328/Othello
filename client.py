'''
Othello remote player for Atomic Object JAR game board
By Abby Peterson, 02/21/24
Functions:
    add_valid_spot() - adds current option to master dictionary if valid
    check_line() - looks at corresponding line of found possible play spot
    search_adjacents() - finds possible play spots next to opponent pieces
    get_move() - searches board and starts funct call^ to dive into all options
    prepare_response() - properly formats chosen spot to send play to server
    get_game_result() - analyzes the final board sent for a winning-odds test file
'''
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
    if cur_val > 0: #this is a space we can play on
        all_options.setdefault(cur_key, 0) #if spot is already an option, this line does nothing
        all_options[cur_key] += cur_val #sum up possible points (may be adding to 0)

def check_line(game_board, rel_loc, start_spot, players, all_opts):
    '''
    PURPOSE: Checks the corresponding row/col/diag of cur empty adj spot to see possible outcome
      If spot is: a corner -- look at the mirrored & extending diag,
      vertical-look at that column (down/up depending), horizontal-look at that row (R/L depending)
    GIVEN: board, adjacent (start) spot and location relative to opp piece found, player and opp #
    RETURNS: None, calls funct to add to all_opt dictionary before choosing which opt in get_move()
    '''
    # Initialize needed variables
    pts = 0
    pos_pts = 0 # possible points when searching along cur row/col/diag
    spot = [-1,-1]
    my_p = players[0]
    opp = players[1]
    r_increment = -1*rel_loc[0] # set depending on type of line we are searching
    c_increment = -1*rel_loc[1] # set depending on type of line we are searching
    r = start_spot[0]
    c = start_spot[1]

    # Checking line loop... spot[r,c] changes as we look WHILE r & c are in range of the board grid
    r+=r_increment
    c+=c_increment
    while 0 <= r < 8 and 0 <= c < 8:
        spot = game_board[r][c]
        if spot == opp:
            pos_pts+=1 #possible piece we can turn
        else:
            if spot == my_p: #valid row play! but counting stops
                pts=pos_pts
            break
        r+=r_increment #new
        c+=c_increment #new
    add_valid_spot(all_opts, (pts, (start_spot[0],start_spot[1])))

def search_adjacents(main_board, row, col, players, all_options):
    '''
    PURPOSE: Check the surrounding area for empty/playable spaces by opponents found piece
      If empty space, call next funct to check corresponding line for possible play stats
    GIVEN: game_board grid, row/col location of opp's piece, who's p1/2, master opts list
    '''
    # Loop through surrounding spots to see open potential spots, careful of edge of board
    for dr in range(-1 if (row > 0) else 0 , 2 if (row < 7) else 1):
        for dc in range(-1 if (col > 0) else 0,2 if (col < 7) else 1):
            cur_r = row+dr
            cur_c = col+dc
            cur_spot = main_board[cur_r][cur_c]
            if cur_spot == 0: # found empty spot adjacent to opp
                check_line(main_board, (dr, dc), (cur_r, cur_c), players, all_options)

def get_move(my_player, cur_board):
    '''
    GIVEN: player: 1 or 2, board: list of game board rows (8x8) -- 0 empty, 1 p-1 spot, 2 p-2 spot
    RETURN: players calculated spot for next play to send -- must be valid option (add brains L8R)
    '''
    opp = 1 # opponents player
    if my_player == 1:
        opp = 2
    all_options = {} #key:spot, val:points - dict sums up overlapping spots! (> old list idea)

    # Determine valid moves...
    # Loop through grid board
    for r in range(8):
        for c in range(8):
            # if found an opponents piece, check adjacent spot where I can potentially play
            if cur_board[r][c] == opp:
                search_adjacents(cur_board, r, c, (my_player, opp), all_options)

    # Now determine best move - greedy strat
    best_opt = (-1,-1) #default invalid
    if len(all_options) != 0: # just incase
        best_opt = max(all_options, key=all_options.get) #returns dict key w/ highest val (pts)
    return [best_opt[0],best_opt[1]] #formatting to a list for sending

def prepare_response(chosen_move):
    '''
    GIVEN: list of len 2 (x,y) for players next move
    RETURN: reformatted move as a JSON array to send as response
    '''
    reformatted = f"{chosen_move}\n".encode() # returns as a JSON array w/newline, Ex: `"[1,2]\n"`
    print(f"sending {reformatted}")
    return reformatted

def get_game_result(p, final_board):
    '''
    PURPOSE: Analyze the final board sent to see who likely won
    GIVEN: p - which player we are, final_board - last JSON result sent before game ended
    RETURN: string result of player's status based on the ending game board (won/tied/lost)
    '''
    p1_spots = sum(row.count(1) for row in final_board)
    p2_spots = sum(row.count(2) for row in final_board)
    if p1_spots+p2_spots < 64:
        print('NOTE: game may have ended early')
    if (p1_spots > p2_spots and p == 1) or (p2_spots > p1_spots and p == 2):
        return "won"
    if p1_spots == p2_spots:
        return "tied"
    return "lost"

if __name__ == "__main__":
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337 # defining port num
    host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname() # host""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initializes socket for connection
    try:
        board = []
        player = 0 # pylint: disable=C0103
        sock.connect((host, port))
        while True:
            data = sock.recv(1024) # Ex. `{"board":[[]],"maxTurnTime":15000,"player":1}\n`
            if not data:
                print('connection to server closed')
                status = get_game_result(player, board) # pylint: disable=C0103
                print(f"Game Over: Player:{player}: {status}") # for testOdds file
                break
            json_data = json.loads(str(data.decode('UTF-8')))
            board = json_data['board']
            maxTurnTime = json_data['maxTurnTime']
            player = json_data['player'] # can be set in terminal command, but never assume val
            print(player, maxTurnTime, board)

            move = get_move(player, board)
            response = prepare_response(move)
            sock.sendall(response)
    finally:
        sock.close() # ends the connection
