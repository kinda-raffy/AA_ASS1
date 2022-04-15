import time
import tabulate
import numpy as np
from dictionary.word_frequency import WordFrequency
from dictionary.list_dictionary import ListDictionary
from dictionary.hashtable_dictionary import HashTableDictionary
from dictionary.ternarysearchtree_dictionary import TernarySearchTreeDictionary


def run_analysis():
    # Read in sampleData200k.txt
    dictionaries = {}
    with open('sampleData200k.txt', 'r') as f:
        sample_data = [line.strip() for line in f.readlines()]
        sample_data = [WordFrequency(word=line.split()[0], frequency=int(line.split()[1])) for line in sample_data]

        for i in range(16):
            prev_size = 200000 // 2 ** (16 - (i - 1))
            size = 200000 // 2 ** (16 - i)
            dictionaries[str(size + prev_size)] = sample_data[:size + prev_size]

    NO_RUNS = 3
    # Build dictionaries.
    dict_sizes, list_times, hash_times, tst_times = list(), list(), list(), list()
    list_dictionary, hash_dict, tst_dict = ListDictionary(), HashTableDictionary(), TernarySearchTreeDictionary()
    # Calculate time taken to build dictionaries.
    for run_no in range(NO_RUNS):
        print(f'Run #{run_no + 1}')
        for index, size in enumerate(dictionaries.keys()):
            print('\tBuilding dictionary of size {}...'.format(size))

            start_time = time.perf_counter_ns()
            list_dictionary.build_dictionary(dictionaries[size])
            list_times.append(list()) if run_no == 0 else None
            list_times[index].append(time.perf_counter_ns() - start_time)

            start_time = time.perf_counter_ns()
            hash_dict.build_dictionary(dictionaries[size])
            hash_times.append(list()) if run_no == 0 else None
            hash_times[index].append(time.perf_counter_ns() - start_time)

            start_time = time.perf_counter_ns()
            tst_dict.build_dictionary(dictionaries[size])
            tst_times.append(list()) if run_no == 0 else None
            tst_times[index].append(time.perf_counter_ns() - start_time)

            dict_sizes.append(size) if run_no == 0 else None
        print()
    # Calculate average times.
    list_avg = [sum(times) / len(times) for times in list_times]
    hash_avg = [sum(times) / len(times) for times in hash_times]
    tst_avg = [sum(times) / len(times) for times in tst_times]
    # Print results.
    print(tabulate.tabulate(np.c_[dict_sizes, list_avg, hash_avg, tst_avg],
                            headers=['Dictionary Size', 'List', 'Hash Table', 'TST'], tablefmt='fancy_grid'))


if __name__ == '__main__':
    run_analysis()
