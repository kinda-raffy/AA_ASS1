import time
from termcolor import colored as c, cprint
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary


# ------------------------------------------------------------------------
# This class is required TO BE IMPLEMENTED. List-based dictionary implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

def log_computation_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        cprint(f"{c(' LIST ', 'cyan', attrs=['bold', 'reverse'])} {c('Computation time', 'magenta')} of"
               f" '{c(func.__name__, 'yellow')}': {c(str(end - start), 'green')}", attrs=['bold'])
        return result
    return wrapper


class ListDictionary(BaseDictionary):
    __slots__ = 'dictionary'

    def __init__(self):
        self.dictionary = []

    # @log_computation_time
    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        for word_frequency in words_frequencies:
            self.dictionary.append(word_frequency)

    # @log_computation_time
    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        for word_frequency in self.dictionary:
            if word_frequency.word == word:
                return word_frequency.frequency
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        # TO BE IMPLEMENTED
        # If word is not in the dictionary than add it to the dictionary.
        if self.search(word_frequency.word) == 0:
            self.dictionary.append(word_frequency)
            return True
        return False

    # @log_computation_time
    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # If word is in the dictionary than delete it from the dictionary.
        for word_frequency in self.dictionary:
            if word_frequency.word == word:
                self.dictionary.remove(word_frequency)
                return True
        return False

    # @log_computation_time
    def autocomplete(self, prefix_word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'prefix_word' as a prefix
        @param prefix_word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'prefix_word'
        """
        # Add words to the frequency_list that have 'prefix_word' as a prefix.
        frequency_list = [word_frequency for word_frequency in self.dictionary
                          if word_frequency.word.startswith(prefix_word)]
        # Sort the list by frequency and return the top 3.
        frequency_list.sort(key=lambda x: x.frequency, reverse=True)
        return frequency_list[:3]
