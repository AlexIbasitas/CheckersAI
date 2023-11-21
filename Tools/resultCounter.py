import subprocess
import datetime

def run_game():
    # Modify the command as needed
    command = [
        'python3', 'AI_Runner.py', '8', '8', '3', 'l',
        '~/CheckersAI/Tools/Sample_AIs/Poor_AI/main.py',
        '~/CheckersAI/src/checkers-python/main.py'
    ]

    # Run the game and capture the output
    result = subprocess.run(command, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



    # Check the result and return 'player 1', 'player 2', or 'tie'
    if 'crashed' in result.stdout:
        return 'crashed'
    if 'player 1 wins' in result.stdout:
        return 'player 1'
    elif 'player 2 wins' in result.stdout:
        return 'player 2'
    elif 'Tie' in result.stdout:
        return 'tie'
    else:
        return 'unrecognized'
    

def main():
    print("Time of program START:", datetime.datetime.now())
    num_games = 100
    player1_wins = 0
    player2_wins = 0
    ties = 0
    crashed_games = 0
    unrecognized_games = 0
    print("Command is as follows: ")
    command = [
    'python3', 'AI_Runner.py', '8', '8', '3', 'l', '~/CheckersAI/src/checkers-python/main.py', '~/CheckersAI/Tools/Sample_AIs/Poor_AI/main.py']
    
    print(command)
    with open("inmain.txt", 'w') as fd: 
        pass

    for i in range(num_games):
        winner = run_game()
        print(i)
        if winner == 'player 1':
            player1_wins += 1
        elif winner == 'player 2':
            player2_wins += 1
        elif winner == 'tie':
            ties += 1
        elif winner == "crashed":
            crashed_games += 1
        elif winner == "unrecognized":
            unrecognized_games += 1


    print("Player 1 Wins: {} ({:.2f}%)".format(player1_wins, (player1_wins / num_games) * 100))
    print("Player 2 Wins: {} ({:.2f}%)".format(player1_wins, (player1_wins / num_games) * 100))
    print("Ties: {} ({:.2f}%)".format(ties, (ties / num_games) * 100))
    print("Crashed Counter:", crashed_games)
    print("Unrecognized counter:", unrecognized_games)
    
    print()
    print("Time of Program End:", datetime.datetime.now())

if __name__ == "__main__":
    main()

