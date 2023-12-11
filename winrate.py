import sys
from statsparser import parse_stats

class Player:
    def __init__(self, name):
        self.name = name
        self.expected_wins = 0
        self.actual_wins = 0
    
    def __str__(self):
        return f"{self.name} won {self.actual_wins} with E(x) of {self.expected_wins}"

def main():
    if len(sys.argv) < 2:
        print("Enter the JSON dump file path as a command line argument.")
        return
    
    parsed_stats = parse_stats(sys.argv[1])
    player_ids = parsed_stats["players"]
    plays = parsed_stats["plays"]

    players = {id: Player(name) for id, name in player_ids.items()}

    for play in plays:
        player_count = len(play.players)
        for player_id in play.players.keys():
            players[player_id].expected_wins += 1 / player_count
            if play.players[player_id]:
                players[player_id].actual_wins += 1
    
    sorted_players = list(players.values())
    sorted_players.sort(key=lambda p: p.actual_wins, reverse=True)
    for player in sorted_players:
        print(player)

if __name__ == '__main__':
    main()