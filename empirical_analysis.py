import sys
import time
from dictionary.node import Node
from dictionary.word_frequency import WordFrequency
from dictionary.base_dictionary import BaseDictionary
from dictionary.list_dictionary import ListDictionary
from dictionary.hashtable_dictionary import HashTableDictionary
from dictionary.ternarysearchtree_dictionary import TernarySearchTreeDictionary


def usage():
    """
    Print help/usage message.
    """
    print('python3 dictionary_file_based.py', '<approach> [data fileName] [command fileName] [output fileName]')
    print('<approach> = <list | hashtable | tst>')
    sys.exit(1)


if __name__ == '__main__':
    # Read in sampleData200k.txt
    dictionaries = {}
    with open('sampleData200k.txt', 'r') as f:
        sampleData = f.readlines()
        sampleData = [line.strip() for line in sampleData]
        sampleData = [WordFrequency(word=line.split()[0], frequency=int(line.split()[1])) for line in sampleData]
        
        for i in range(16):
            prev_size = 200000 // 2 ** (16 - (i - 1))
            size = 200000 // 2 ** (16 - i)
            dictionaries[str(size + prev_size)] = sampleData[:size + prev_size]

    # Build dictionaries.
    list_times = []
    hash_times = []
    tst_times = []
    dict_sizes = []
    listDictionary = ListDictionary()
    hashDictionary = HashTableDictionary()
    tstDictionary = TernarySearchTreeDictionary()
    iterations = 10
    for key, value in dictionaries.items():
        print('Building dictionaries with size:', key)
        dict_sizes.append(key)
        start_time = time.perf_counter_ns()
        listDictionary.build_dictionary(value)
        end_time = time.perf_counter_ns()
        list_times.append(end_time - start_time)

        start_time = time.perf_counter_ns()
        hashDictionary.build_dictionary(value)
        end_time = time.perf_counter_ns()
        hash_times.append(end_time - start_time)

        start_time = time.perf_counter_ns()
        tstDictionary.build_dictionary(value)
        end_time = time.perf_counter_ns()
        tst_times.append(end_time - start_time)

    for i in range(iterations-1):
        print('Iteration', i+2)
        for key, value in dictionaries.items():
            iter = dict_sizes.index(key)
            start_time = time.perf_counter_ns()
            listDictionary.build_dictionary(value)
            end_time = time.perf_counter_ns()
            list_times[iter] = (list_times[iter] + end_time - start_time)

            start_time = time.perf_counter_ns()
            hashDictionary.build_dictionary(value)
            end_time = time.perf_counter_ns()
            hash_times[iter] = (hash_times[iter] + end_time - start_time)

            start_time = time.perf_counter_ns()
            tstDictionary.build_dictionary(value)
            end_time = time.perf_counter_ns()
            tst_times[iter] = (tst_times[iter] + end_time - start_time)

    list_times = [i/iterations for i in list_times]
    hash_times = [i/iterations for i in hash_times]
    tst_times  = [i/iterations for i in  tst_times]
    list_times.pop(0)
    hash_times.pop(0)
    tst_times.pop(0)
    dict_sizes.pop(0)

    print(dict_sizes)
    print(list_times)
    print(hash_times)
    print(tst_times)
