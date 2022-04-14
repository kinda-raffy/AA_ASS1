from treelib import Node, Tree
from termcolor import colored as c, cprint
import time

from dictionary.base_dictionary import BaseDictionary
from dictionary.word_frequency import WordFrequency
from dictionary.node import Node


# ------------------------------------------------------------------------
# This class is required to be implemented. Ternary Search Tree implementation.
#
# __author__ = 'Son Hoang Dau'
# __copyright__ = 'Copyright 2022, RMIT University'
# ------------------------------------------------------------------------

def log_computation_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        cprint(f"{c(' TST ', 'cyan', attrs=['bold', 'reverse'])} {c('Computation time', 'magenta')} of"
               f" '{c(func.__name__, 'yellow')}': {c(str(end - start), 'green')}", attrs=['bold'])
        return result
    return wrapper


class TernarySearchTreeDictionary(BaseDictionary):
    __slots__ = 'root_'

    def __init__(self):
        self.root_ = None

    @log_computation_time
    def build_dictionary(self, words_frequencies: [WordFrequency]):
        """
        construct the data structure to store nodes
        @param words_frequencies: list of (word, frequency) to be stored
        """
        for word_frequency in words_frequencies:
            self.add_word_frequency(word_frequency)

        # self.print_tree(self.root_)

    # @log_computation_time
    def search(self, word: str, return_node=False, return_parent=False) -> int:
        """
        search for a word
        @param word: the word to be searched
        @return: frequency > 0 if found and 0 if NOT found
        """
        curr = self.root_
        parent = None
        # Return 0 if the tree or word is empty.
        if self.root_ is None or word == '':
            return 0
        dict_word = ''
        letter_index = 0
        letter = word[letter_index]

        # Search for the word.
        while curr is not None:
            # If the current letter is the same as the word, add it to the dictionary word and explore middle.
            if letter == curr.letter:
                dict_word += letter
                # If the word has been built, return the frequency.
                if dict_word == word and (curr.end_word if not return_node else True):
                    return curr.frequency if not return_node else (curr.frequency, curr)\
                    if not return_parent else (curr.frequency, curr, parent)
                letter_index += 1
                try:
                    letter = word[letter_index]
                except IndexError:
                    return 0
                parent = curr
                curr = curr.middle
            # If the letter is smaller than the current letter, go left.
            elif letter < curr.letter:
                parent = curr
                curr = curr.left
            # If the letter is greater than the current letter, go right.
            elif letter > curr.letter:
                parent = curr
                curr = curr.right
            
        return 0

    def add_word_frequency(self, word_frequency: WordFrequency) -> bool:
        """
        add a word and its frequency to the dictionary
        @param word_frequency: (word, frequency) to be added
        :return: True whether succeeded, False when word is already in the dictionary
        """
        word = word_frequency.word
        frequency = word_frequency.frequency
        # Return False if the word is already in the tree.
        if self.search(word_frequency.word) > 0:
            return False
        letter_index = 0
        # If the tree is empty; else if the tree is not empty.
        if self.root_ is None:
            self.root_ = Node(word[letter_index]) if len(word) != 1 else Node(word[letter_index], frequency, True)
            letter_index += 1
            parent = self.root_
        else:
            parent = None
            iter_node = self.root_
            while parent is None:
                # Grab the letter of the current iteration.
                letter = word[letter_index]
                # Explore left branch.
                if letter < iter_node.letter:
                    # Set iter to left child if not empty, else, create a new node.
                    if iter_node.left is not None and letter_index < len(word) - 1:
                        iter_node = iter_node.left
                    else:
                        iter_node.left = self.grab_parent_node(word, frequency, letter_index)
                        parent = iter_node.left
                        letter_index += 1
                # Explore right branch.
                elif letter > iter_node.letter:
                    # Set iter to right child if not empty, else, create a new node.
                    if iter_node.right is not None and letter_index < len(word) - 1:
                        iter_node = iter_node.right
                    else:
                        iter_node.right = self.grab_parent_node(word, frequency, letter_index)
                        parent = iter_node.right
                        letter_index += 1
                # Explore middle branch.
                elif letter == iter_node.letter:
                    # Set iter to middle child if not empty, else, set parent to current iter_node.
                    if iter_node.middle is not None and letter_index < len(word) - 1:
                        iter_node = iter_node.middle
                        letter_index += 1
                    else:
                        if letter_index == len(word) - 1:
                            iter_node.frequency = frequency
                            iter_node.end_word = True
                        parent = iter_node
                        letter_index += 1
        # Add the remaining letters to the middle branch.
        for i, letter in enumerate(word[letter_index:], start=letter_index):
            current = Node(letter) if i < (len(word) - 1) else Node(letter=letter, frequency=frequency, end_word=True)
            parent.middle = current
            parent = current
        return True

    @log_computation_time
    # Refresh the tree by pruning dead ends.
    def refresh_tree(self):
        def prune(node, parent):
            if node:
                # If the leaf is a dead end, remove it.
                if self.dead_child(node):
                    if parent.middle is node:
                        parent.middle = None
                    elif parent.left is node:
                        parent.left = None
                    elif parent.right is node:
                        parent.right = None
                else:
                    prune(node.left, node)
                    prune(node.right, node)
                    prune(node.middle, node)
        prune(self.root_, None)

    @log_computation_time
    # FIXME - Delete word fails to delete when the last letter is not a dead-end (and is connected to other valid
    #  nodes). In this case, end_word should just be set to False.
    def delete_word(self, word: str) -> bool:
        """
        delete a word from the dictionary
        @param word: word to be deleted
        @return: whether succeeded, e.g. return False when point not found
        """
        # TO BE IMPLEMENTED

        # Recursive Implementation. We need to delete end nodes that are not part of another word.
        # We will begin at the start of the word, and recursively look for the correct child node.
        # We cull this node if the child recursive call returns True, and this node has no other children.

        return_value = False

        if word == '':
            return False

        def _delete_word(curr: Node, parent: Node, letters) -> bool:

            # If this node is empty, it counts as deleted.
            if curr is None:
                return True
            # If node is not empty and string is empty, not deleted.
            if letters == "":
                return False  
            # If this node is valid to be deleted
            valid = True
            # if this node is th next part of the word
            if curr.letter == letters[0]:
                if len(letters) == 1:
                    valid = _delete_word(curr.middle, curr, "")
                else:
                    # Try to delete middle
                    valid = _delete_word(curr.middle, curr, letters[1:])
                if valid:
                    curr.middle = None
            else:
                valid = False

            if _delete_word(curr.left, curr, letters):
                curr.left = None
            else:
                valid = False
            if _delete_word(curr.right, curr, letters):
                curr.right = None
            else:
                valid = False

            
            # if L,M,R all deleted or None and this is part of word
            if valid:
                del curr
                # set global success to True
                nonlocal return_value
                return_value = True
                return True
            else:
                return False

        try:
            _, startNode, startParent = self.search(word[0], return_node=True, return_parent=True)
        except(TypeError):
            return False

        if startNode is None:
            return False
    
        _delete_word(startNode, startParent, word)
        self.refresh_tree()

        if word == 'cute':
            self.print_tree(self.root_)
        
        return return_value

    @log_computation_time
    def autocomplete(self, word: str) -> [WordFrequency]:
        """
        return a list of 3 most-frequent words in the dictionary that have 'word' as a prefix
        @param word: word to be autocompleted
        @return: a list (could be empty) of (at most) 3 most-frequent words with prefix 'word'
        """
        return_list = list()
        # Return if word is empty.
        if word == str():
            return return_list
        # Search for the prefix
        try:
            _, prefixes_suffix = self.search(word, return_node=True)
        # Return if prefix not found.
        except TypeError:
            return return_list
        # If prefix is a word itself, add it to the list.
        if prefixes_suffix.end_word:
            return_list.append(WordFrequency(word, prefixes_suffix.frequency))

        def recursive_search(curr: Node, w):
            # If end of the tree is reached, return.
            if curr is None:
                return
            # If this is a word, add it to the list.
            if curr.end_word:
                return_list.append(WordFrequency(w + curr.letter, curr.frequency))
            # If this is a prefix, search for the word.
            recursive_search(curr.left, w)
            recursive_search(curr.middle, w + curr.letter)
            recursive_search(curr.right, w)
        # Call recursive search.
        recursive_search(prefixes_suffix.middle, word)
        # Sort the list by frequency and return top 3.
        return_list.sort(key=lambda x: x.frequency, reverse=True)
        return return_list[:3]
    
    @staticmethod
    def dead_child(n: Node) -> bool:
        return n.left is None and n.right is None and n.middle is None and n.frequency is None and n.end_word is False

    @staticmethod
    def grab_parent_node(w: str, f: int, i: int) -> Node:
        return Node(letter=w[i]) if (len(w) - 1) != i else Node(letter=w[i], frequency=f, end_word=True)

    @staticmethod
    def print_tree(curr_: Node) -> None:
        tree = Tree()

        def pre_order_traversal(curr, parent):
            # Set nodes to be printed.
            if curr:
                if parent is None:
                    parent = tree.create_node(c(f"({(curr.letter.capitalize())}, {curr.frequency}, {curr.end_word})", 'blue', attrs=['bold', 'reverse']))
                else:
                    parent = tree.create_node(f"({c(curr.letter.capitalize(), 'blue', attrs=['bold'])}, {curr.frequency}, {c(curr.end_word, ('green' if curr.end_word else 'red'))})", parent=parent)
                # Recursive call.
                pre_order_traversal(curr.left, parent)
                pre_order_traversal(curr.middle, parent)
                pre_order_traversal(curr.right, parent)

        # Call recursive function.
        pre_order_traversal(curr_, None)
        cprint("\n========================== TST ==========================", 'cyan')
        tree.show(reverse=False)


def debug():
    wf_dict = [WordFrequency('cut', 10),
               WordFrequency('app', 20),
               # WordFrequency('pneumonoultramicroscopicsilicovolcanoconiosis', 20),
               WordFrequency('cute', 50),
               WordFrequency('comfy', 100),
               WordFrequency('couch', 500),
               WordFrequency('computer', 90),
               WordFrequency('adrian', 69),
               WordFrequency('raf', 50),
               WordFrequency('farm', 40),
               WordFrequency('cup', 30)]

    tst = TernarySearchTreeDictionary()
    tst.build_dictionary(wf_dict)
    # tst.delete_word('app')
    tst.print_tree(curr_=tst.root_)
    [print(x.word, x.frequency) for x in tst.autocomplete('cut')]


if __name__ == '__main__':
    debug()
