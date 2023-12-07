import json

summary_indent = 2

# Simple data structure for the summarise() function. Behaves like a tree node.
class SummaryLine:
    def __init__(self):
        self.statement = ""
        self.sublines = []
        self.indent = 0
    
    def increase_indent(self):
        self.indent += summary_indent
        for subline in self.sublines:
            subline.increase_indent()

# Simple data structure representing an instance of a game being played.
# Designed to be used in conjunction with player and game ID maps, so that
# it's not all just meaningless numbers.
class Play:
    def __init__(self, data, player_map, game_map):
        self.date_string = data["playDate"]
        # TODO: self.date, i.e. a useful date object
        self.players = {} # Map of player IDs to whether or not they won
        for player in data["playerScores"]:
            self.players[player["playerRefId"]] = player["winner"]
        self.game = data["gameRefId"]
        self.player_map = player_map
        self.game_map = game_map
    
    # This will break if player_map and game_map aren't full first
    def __str__(self):
        string = f"Play of {self.game_map[self.game]} on {self.date_string}:\n"
        for id, won in self.players.items():
            string += f"    {self.player_map[id]}: "
            string += "WINNER!!!!!" if won else "loser...."
            string += "\n"
        return string

# Parses the stats into a reasonable format.
def parse_stats(filename):
    result = {}
    with open(filename, 'r', encoding='UTF-8') as f:
        raw = json.load(f)
        players = parse_id_list(raw["players"])
        games = parse_id_list(raw["games"])
        plays = []
        for play in raw["plays"]:
            plays.append(Play(play, players, games))
        result["players"] = players
        result["games"] = games
        result["plays"] = plays
    return result

# Builds a map of IDs to names using list data.
# Conveniently works for both players and games.
def parse_id_list(data_list):
    return {item["id"]: item["name"] for item in data_list}

# Produces a string summary of raw dict/list data.
def get_structure_summary(data):
    summary_tree = summarise(data)
    summary_string = compile_summary(summary_tree)
    return summary_string

# Recursively produces a tree of SummaryLines for simple summary printing.
def summarise(data):
    summary_line = SummaryLine()
    
    if isinstance(data, list):
        if len(data):
            summary_line.statement = "List of"
            subline = summarise(data[0])
            subline.increase_indent()
            summary_line.sublines.append(subline)
        else:
            summary_line.statement = "Empty list"
    
    elif isinstance(data, dict):
        summary_line.statement = "Object of"
        for key, contents in data.items():
            subline = summarise(contents)
            subline.increase_indent()
            subline.statement = key + ": " + subline.statement
            summary_line.sublines.append(subline)
    
    else:
        summary_line.statement = str(type(data))
    
    return summary_line

# Traverse a tree of SummaryLines to compile them into a string.
def compile_summary(summary_line):
    summary_string = summary_line.indent * " " + summary_line.statement + "\n"
    for subline in summary_line.sublines:
        summary_string += compile_summary(subline)
    return summary_string

def main():
    file_path = input("Enter relative file path: ")
    parsed_stats = parse_stats(file_path)
    for play in parsed_stats["plays"]:
        print(play)

if __name__ == '__main__':
    main()