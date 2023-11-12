import subprocess

def run_game():
    # Modify the command as needed
    command = [
        'python3', 'AI_Runner.py', '8', '8', '3', 'l',
        '~/CheckersAI/Tools/Sample_AIs/Random_AI/main.py',
        '~/CheckersAI/src/checkers-python/main.py'
    ]

    # Run the game and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Check the result and return 'player 1', 'player 2', or 'tie'
    
    if 'player 1 wins' in result.stdout:
        return 'player 1'
    elif 'player 2 wins' in result.stdout:
        return 'player 2'
    elif 'Tie' in result.stdout:
        return 'tie'
    else:
        return 'unknown'

def main():
    num_games = 100
    player1_wins = 0
    player2_wins = 0
    ties = 0
    unknown_games = 0
    print("in main")
    for i in range(num_games):
        winner = run_game()
        print(i)
        if winner == 'player 1':
            player1_wins += 1
        elif winner == 'player 2':
            player2_wins += 1
        elif winner == 'tie':
            ties += 1
        elif winner == "unknown":
            unknown_games += 1


    print(f"Player 1 Wins: {player1_wins} ({(player1_wins / num_games) * 100:.2f}%)")
    print(f"Player 2 Wins: {player2_wins} ({(player2_wins / num_games) * 100:.2f}%)")
    print(f"Ties: {ties} ({(ties / num_games) * 100:.2f}%)")
    print("Unknown Counter:", unknown_games)
if __name__ == "__main__":
    main()