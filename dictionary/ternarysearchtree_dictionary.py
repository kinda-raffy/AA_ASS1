from treelib import Node, Tree

from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
from dictionary.node import Node


# ------------------------------------------------------------------------
# This class is required to be implemented. Ternary Search Tree implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------


class TernarySearchTreeDictionary(BaseDictionary):
    __slots__ = 'root_'

    def __init__(self):
        # Initialise the tree
        self.root_ = None

    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        # TO BE IMPLEMENTED

        for word_frequency in words_frequencies:
            self.add_word_frequency(word_frequency)

    def search(self, word: str) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        # Check if the tree is empty.
        if self.root_ is None:
            return 0
        # Search for the word.
        dict_word = ''
        letter_index = 0
        letter = word[letter_index]
        curr = self.root_
        while curr is not None:
            if letter == curr.letter:
                dict_word += letter
                if dict_word == word:
                    return curr.frequency
                letter_index += 1
                letter = word[letter_index]
                curr = curr.middle
            elif letter < curr.letter:
                curr = curr.left
            elif letter > curr.letter:
                curr = curr.right
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        letter_index = 0
        word = word_frequency.word
        frequency = word_frequency.frequency
        if self.root_ is None:
            self.root_ = Node(letter=word[letter_index]) if len(word) != 1 \
                else Node(letter=word[letter_index], frequency=frequency, end_word=True)
            letter_index += 1
            parent = self.root_
        else:
            parent = None
            iter_node = self.root_
            while parent is None:
                letter = word[letter_index]
                if letter < iter_node.letter:
                    if iter_node.left is not None:
                        iter_node = iter_node.left
                    else:
                        iter_node.left = self.grab_parent_node(word, frequency, letter_index)
                        parent = iter_node.left
                        letter_index += 1
                elif letter > iter_node.letter:
                    if iter_node.right is not None:
                        iter_node = iter_node.right
                    else:
                        iter_node.right = self.grab_parent_node(word, frequency, letter_index)
                        parent = iter_node.right
                        letter_index += 1
                elif letter == iter_node.letter:
                    if iter_node.middle is not None:
                        iter_node = iter_node.middle
                        letter_index += 1
                    else:
                        parent = iter_node
                        letter_index += 1

        for i, letter in enumerate(word[letter_index:], start=letter_index):
            current = Node(letter) if i < (len(word) - 1) else Node(letter=letter, frequency=frequency, end_word=True)
            parent.middle = current
            parent = current

        # return True
        # place holder for return
        # return False

    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return False

    def autocomplete(self, word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return []

    @staticmethod
    def grab_parent_node(w, f, i):
        return Node(letter=w[i]) if (len(w) - 1) != i else Node(letter=w[i], frequency=f, end_word=True)

    @staticmethod
    def print_tree(curr_) -> None:
        tree = Tree()

        def pre_order_traversal(curr, parent):
            # Set nodes to be printed.
            if curr:
                if parent is None:
                    parent = tree.create_node(f"({curr.letter.capitalize()}, {curr.frequency}, {curr.end_word})")
                else:
                    parent = tree.create_node(f"({curr.letter.capitalize()}, {curr.frequency}, {curr.end_word})",
                                              parent=parent)
                # Recursive call.
                pre_order_traversal(curr.left, parent)
                pre_order_traversal(curr.middle, parent)
                pre_order_traversal(curr.right, parent)
        # Call recursive function.
        pre_order_traversal(curr_, None)
        tree.show(reverse=False)


def debug():
    """
    A function to test the implementation of the Ternary Search Tree
    """
    tst = TernarySearchTreeDictionary()
    tst.build_dictionary([WordFrequency('cut', 10), WordFrequency('app', 20),
                          WordFrequency('cute', 50), WordFrequency('farm', 40), WordFrequency('cup', 30)])
    tst.print_tree(curr_=tst.root_)
    print(f" cut - {tst.search('cut')}\n"
          f" raf - {tst.search('raf')}")


if __name__ == '__main__':
    debug()
