import subprocess
import time

#RESULTS 2/25
#   70% as p1 out of 10
#   71% as p1 out of 100
#   66% as p2 out of 100
#   69.35% p2 out of 310
#   70% as p1 out of 120

def best_of_100_games():
    port = '1337' # or 1338 for p2
    player = 0 #default
    remote_player_wins = 0
    ties = 0
    for ctr in range(0,100):
        time.sleep(5) # waits 5 seconds so server is ready fs
        print('NEW Game {!r} Starting!...'.format(ctr))
        result = subprocess.run(['python', 'client.py', port], capture_output=True, text=True) # connects to gameboard server to play game
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if line.startswith("Game Over:"):
                print('LINE: {}'.format(line))
                info = line.split(":")[2:] # [player, result]
                player = info[0].strip()
                result = info[1].strip()
                if result == "won":
                    print('P{!r} won!'.format(player))
                    remote_player_wins += 1
                elif result == "tied":
                    print('P{!r} tied!'.format(player))
                    ties += 1
                else:
                    print('P{!r} lost.'.format(player))
    return ctr, player, remote_player_wins, ties

if __name__ == "__main__":
    ctr, player, total_wins, total_ties = best_of_100_games()
    print('Player {!r} won: {!r}/{!r} and tied: {!r}/{!r}'.format(player, total_wins, ctr+1, total_ties, ctr+1))
    print('WIN PERCENTAGE: {}'.format(100*(total_wins/(ctr+1))))
