from random import choice, randint

from matplotlib.cbook import file_requires_unicode
from HangmanGame import HangmanGame



class Word(HangmanGame):
    def __init__(self):
        super().__init__()
        self._word = self.set_word()
        l = len(self._word)
        self._freq_chars_total_hide = int((l/2)/l*100)
        self.freq_chars_to_find = 0
        self.freq_chars_foundt = 0
        self._word_with_hidden_characters = ""#self._set_word_with_hidden_characters()
        
        self.list_chars_tryed = []
        
    def _set_word_with_hidden_characters(self):
        # self._word_with_hidden_characters = self._word
        list_chars_from_word = []
        for c in self._word:
            list_chars_from_word.append(c)
        
        while self.freq_chars_to_find != self._freq_chars_total_hide:
            index = randint(0, len(self._word)-1)
            if not list_chars_from_word[index] == self._hide_char:
                list_chars_from_word[index] = self._hide_char
                self.freq_chars_to_find += 10
        
        self._word_with_hidden_characters = "".join(list_chars_from_word)
    
    def add_char_to_list_tryed(self, c:str):
        if not c in self.list_chars_tryed:
            self.list_chars_tryed.append(c)
    
    def refresh_word(self, char_typed:str):
        list_chars_from_word = []
        index = 0
        for c in self._word_with_hidden_characters:
            list_chars_from_word.append(c)
            
        # if char_typed in self._word:
        #     index = self._word[char_typed]
        index = 0
        for c in self._word:
            if self._word[index] == char_typed:
                if list_chars_from_word[index] == self._hide_char:
                    list_chars_from_word[index] = c
                    self.freq_chars_foundt += 10
                    
            index += 1
        self._word_with_hidden_characters = "".join(list_chars_from_word)
    
    def check_win(self):
        return (self.freq_chars_foundt >= self.freq_chars_to_find)
    
    def get_chars_tryed(self):
        return ";".join(self.list_chars_tryed)
    
    def set_word(self):
        return choice(self._list_word)
 