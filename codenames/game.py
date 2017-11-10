# object for tracking game status
import random
import json

# dictionaries
FILE_ROOT="/Users/jporter/code/codenames"
DICTIONARIES={
    "CAH" :         FILE_ROOT + "/cah_code_names.txt", 
    "Pop Culture" : FILE_ROOT + "/code_names_pop.txt", 
    "Dictionary" :  FILE_ROOT + "/code_names_dict.txt", 
    "Simple" :      FILE_ROOT + "/code_names_simple.txt"
}
# colors per team
RED = 'R'
BLUE = 'B'
GREEN = 'G'
# num words per board
NUM_WORDS_NORMAL=25
NUM_WORDS_BIG=81
BIG_BLACKOUT_SPOTS=[4,20,24,36,40,44,56,60,76]

class Info:
    def __init__(self, game_id=1, dictionary='Dictionary', seed=None, size=NUM_WORDS_NORMAL, teams=2):
        self.game_id = game_id
        self.size = size
        self.starting_color = RED
        self.teams = teams
        self.players = []
        self.dictionary = dictionary
        self.dictionaries = DICTIONARIES.keys()
        self.words = self.__get_words()
        self.layout = self.__get_layout()
        self.board = dict.fromkeys(self.words, False)
        self.solution = dict(zip(self.words, self.layout))

    def to_json(self):
        return {
            "game_id": self.game_id,
            "starting_color": self.starting_color,
            "players": self.players,
            "words": self.words,
            "board": self.board,
            "layout": self.layout,
            "solution": self.solution,
        }

    def flip_card(self, word):
        if word not in self.words:
            return 'Invalid word entered.'
        self.board[word] = self.solution[word]
        return self.solution[word]

    def add_player(self, name):
        self.players.append(name)
        
    def remove_player(self, name):
        self.players.remove(name)

    def __get_words(self):
        if not self.dictionary in DICTIONARIES.keys():
            print ("Error: dictionary '" + self.dictionary + "' doesn't exist")
            return None
        words_file = open(DICTIONARIES[self.dictionary], 'r')
        words = [elem for elem in words_file.read().split('\n') if len(elem.strip()) > 0]
        random.shuffle(words)
        final_words = words[0:self.size]
        return final_words

    def __get_layout(self):
        self.starting_color = RED
        green = 0
        if self.size == NUM_WORDS_NORMAL:
            if self.teams==3:
                blue = 5
                red = 5
                green = 5
            else:
                blue = 8
                red = 8

            bystanders = 25 - blue - red - green - 2
        else:
            if self.teams == 2:
                blue = 8
                red = 8
            elif self.teams == 3:
                blue = 8
                red = 8
                green = 8
            num_blackouts = 9
            bystanders = 81 - num_blackouts - blue - red - green - 3
        if self.teams == 2:
            if random.random() < 0.5:
                blue += 1
                self.starting_color = BLUE
            else:
                red += 1
        else:
            if random.random() < 0.333:
                blue += 1
                self.starting_color = BLUE
            elif random.random() > 0.666:
                green += 1
                self.starting_color = GREEN
            else:
                red += 1
        mix = ["B"] * blue
        mix.extend(["R"] * red)
        if green > 0:
            mix.extend(['G'] * green)
        mix.extend(["X"])
        if self.size == NUM_WORDS_BIG:
            mix.extend(['X'])
        mix.extend(["O"] * bystanders)
        random.shuffle(mix)
        if self.size == NUM_WORDS_BIG:
            for i in BIG_BLACKOUT_SPOTS:
                mix.insert(i, '-')
        return mix

