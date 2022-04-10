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


def print_tree(curr_) -> None:
    tree = Tree()

    def pre_order_traversal(curr, parent):
        if curr:
            if parent is None:
                parent = tree.create_node(curr.letter.capitalize())
            else:
                parent = tree.create_node(curr.letter.capitalize(), parent=parent)

            pre_order_traversal(curr.left, parent)
            pre_order_traversal(curr.middle, parent)
            pre_order_traversal(curr.right, parent)

    pre_order_traversal(curr_, None)
    tree.show(reverse=False)


class TernarySearchTreeDictionary(BaseDictionary):

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
        # TO BE IMPLEMENTED
        # place holder for return
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        letter_index = 0
        if self.root_ is None:
            self.root_ = Node(letter=word_frequency.word[letter_index]) if len(word_frequency.word) != 1 \
                else Node(letter=word_frequency.word[letter_index], frequency=word_frequency.frequency, end_word=True)
            letter_index += 1
            root = self.root_
        else:
            root = None
            iter_node = self.root_
            while root is None:
                letter = word_frequency.word[letter_index]
                if letter < iter_node.letter:
                    if iter_node.left is not None:
                        iter_node = iter_node.left
                    else:
                        iter_node.left = Node(letter=letter)
                        root = iter_node.left
                        letter_index += 1
                elif letter > iter_node.letter:
                    if iter_node.right is not None:
                        iter_node = iter_node.right
                    else:
                        iter_node.right = Node(letter=letter)
                        root = iter_node.right
                        letter_index += 1
                elif letter == iter_node.letter:
                    if iter_node.middle is not None:
                        iter_node = iter_node.middle
                        letter_index += 1
                    else:
                        root = iter_node
                        letter_index += 1

        # FIXME - Will this run with single words?
        for i, letter in enumerate(word_frequency.word[letter_index:], start=letter_index):
            current = Node(letter=letter) if i < len(word_frequency.word) - 1 \
                else Node(letter=letter, frequency=word_frequency.frequency, end_word=True)
            root.middle = current
            root = current


            # TO BE IMPLEMENTED
            # # Add first letter to tree if it doesn't exist.
            # if self.root is None:
            #     # Set parent to root.
            #     self.root = Node(letter=word_frequency.word[0], frequency=None, end_word=False)
            #     parent = self.root
            # else:
            #     letter = word_frequency.word[0]
            #     iter_node = self.root
            #     # Set parent to last available prefix letter in the tree.
            #     while True:
            #         # If letter is found, set parent to that node.
            #         if letter == iter_node.letter:
            #             parent = iter_node
            #             break
            #         # If letter is lower than current iteration, move left.
            #         elif letter < iter_node.letter:
            #             # If left child is None, create new node; else iterate through left child.
            #             if iter_node.left is None:
            #                 iter_node.left = Node(letter=letter, frequency=None, end_word=False)
            #                 parent = iter_node.left
            #                 break
            #             else:
            #                 iter_node = iter_node.left
            #         # If letter is higher than current iteration, move right.
            #         elif letter > iter_node.letter:
            #             # If right child is None, create new node; else iterate through right child.
            #             if iter_node.right is None:
            #                 iter_node.right = Node(letter=letter, frequency=None, end_word=False)
            #                 parent = iter_node.right
            #                 break
            #             else:
            #                 iter_node = iter_node.right
            #         pass
            #
            # # Add rest of the word to tree.
            # for i, letter in enumerate(word_frequency.word[1:]):
            #     # Set the current node to the current letter.
            #     current = Node(letter=letter, frequency=None, end_word=False) if i < len(word_frequency.word) - 2 \
            #         else Node(letter=letter, frequency=word_frequency.frequency, end_word=True)
            #     # Add the current node to the tree.
            #     parent.middle(current)
            #     # if letter > parent.letter:
            #     #     parent.right = current
            #     # elif letter < parent.letter:
            #     #     parent.left = current
            #     # elif letter == parent.letter:
            #     #     parent.middle = current
            #     # Set the parent node to the current node for next iterations.
            #     parent = current

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

    def autocomplete(self, word: str) -> [str]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        # TO BE IMPLEMENTED
        # place holder for return
        return []


def debug():
    """
    A function to test the implementation of the Ternary Search Tree
    """
    tst = TernarySearchTreeDictionary()
    tst.build_dictionary([WordFrequency('cut', 10), WordFrequency('app', 20),
                          WordFrequency('cute', 50), WordFrequency('farm', 40), WordFrequency('cup', 30)])
    print_tree(curr_=tst.root_)


if __name__ == '__main__':
    debug()
