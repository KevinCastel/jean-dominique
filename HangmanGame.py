class HangmanGame(object):
    def __init__(self):
        self._list_word = [
            "programmation",
            "développement",
            "jeux",
            "ordinateur",
            "mot",
            "trouver"]
                
        self._difficulty = 50
        self._hide_char = "$"
