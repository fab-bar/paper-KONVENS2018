import argparse
from collections import defaultdict
import csv
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('trainfile')
    parser.add_argument('develfile')
    parser.add_argument('testfile')
    parser.add_argument('tok_column', type=int)
    parser.add_argument('first_word_column', type=int)
    parser.add_argument('last_word_column', type=int)

    parser.add_argument('spellvardict')
    parser.add_argument('traintoken')
    parser.add_argument('traindict')
    parser.add_argument('develdict')
    parser.add_argument('testdict')
    args, _ = parser.parse_known_args()


    tokens = []
    types_for_word = defaultdict(set)
    words_for_type = defaultdict(set)
    known_types = set()

    with open(args.trainfile, 'r') as input_file:
        for tok_line in csv.reader(input_file, delimiter='\t', quoting=csv.QUOTE_NONE):
            if tok_line:
                word = '_'.join(tok_line[(args.first_word_column - 1):args.last_word_column])
                ttype = tok_line[args.tok_column - 1]
                tokens.append({'type': ttype})

                types_for_word[word].add(ttype)
                words_for_type[ttype].add(word)
                known_types.add(ttype)


    spellvardict = defaultdict(set)
    for ttype in words_for_type.keys():
        for word in words_for_type[ttype]:
            spellvardict[ttype].update(types_for_word[word] - set([ttype]))


    ## get unknown types from test_data
    def get_unknown_from_file(filename, known_types, first_word_column, last_word_column, tok_column):

        unknown_types = set()

        with open(filename, 'r') as input_file:
            for tok_line in csv.reader(input_file, delimiter='\t', quoting=csv.QUOTE_NONE):
                if tok_line:
                    word = '_'.join(tok_line[(first_word_column - 1):last_word_column])
                    ttype = tok_line[tok_column - 1]

                    unknown_types.add(ttype)

        return unknown_types - known_types

    devel_types = get_unknown_from_file(args.develfile, known_types,
                                       args.first_word_column, args.last_word_column, args.tok_column)
    test_types = get_unknown_from_file(args.testfile, known_types,
                                       args.first_word_column, args.last_word_column, args.tok_column)

    json.dump(tokens, open(args.traintoken, 'w'))
    json.dump(sorted(known_types), open(args.traindict, 'w'))
    json.dump(sorted(devel_types), open(args.develdict, 'w'))
    json.dump(sorted(test_types), open(args.testdict, 'w'))
    json.dump({ttype: sorted(variants) for ttype, variants in spellvardict.items()}, open(args.spellvardict, 'w'))
