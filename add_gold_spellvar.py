import argparse
from collections import defaultdict
import csv

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('trainfile')
    parser.add_argument('testfile')
    parser.add_argument('tok_column', type=int)
    parser.add_argument('first_word_column', type=int)
    parser.add_argument('last_word_column', type=int)
    args, _ = parser.parse_known_args()

    worddict = defaultdict(lambda: defaultdict(int))
    known_types = set()

    with open(args.trainfile, 'r') as input_file:
        for tok_line in csv.reader(input_file, delimiter='\t', quoting=csv.QUOTE_NONE):
            if tok_line:
                word = '_'.join(tok_line[(args.first_word_column - 1):args.last_word_column])
                worddict[word][tok_line[args.tok_column - 1]] += 1
                known_types.add(tok_line[args.tok_column -1])

    spellvardict = {word: max(types, key=types.get) for word, types in worddict.items()}


    with open(args.testfile, 'r') as input_file:
        for tok_line in csv.reader(input_file, delimiter='\t', quoting=csv.QUOTE_NONE):
            if tok_line:
                if (tok_line[args.tok_column-1] not in known_types) and ('_'.join(tok_line[(args.first_word_column - 1):args.last_word_column]) in worddict):
                    print('\t'.join(tok_line + [spellvardict['_'.join(tok_line[(args.first_word_column - 1):args.last_word_column])]]))
                else:
                    print('\t'.join(tok_line + [tok_line[args.tok_column-1]]))
            else:
                print()

