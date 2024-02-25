import subprocess
import time

def best_of_100_games():
    port = '1337' # or 1338
    player = 0 #default
    remote_player_wins = 0
    ties = 0
    for ctr in range(0,100):
        time.sleep(5) # waits 5 seconds
        result = subprocess.run(['python', 'client.py', port], capture_output=True, text=True) # connects to gameboard server to play game
        output_lines = result.stdout.split('\n')
        for line in output_lines:
            if line.startswith("Game Over:"):
                info = line.split(":")[2:] # [player, result]
                player = info[0].strip()
                if info[1].strip() == "won":
                    remote_player_wins += 1
                elif info[1].strip() == "tied":
                    ties += 1
    return ctr, player, remote_player_wins, ties

if __name__ == "__main__":
    ctr, player, total_wins, total_ties = best_of_100_games()
    print('Player {!r} won: {!r}/{!r} and tied: {!r}/{!r}'.format(player, total_wins, ctr, total_ties, ctr))