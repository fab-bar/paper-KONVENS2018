## McNemar test
import argparse
import csv
import math

from scipy import stats

import experiment_settings
import eval

def get_mc_nemar_stats(gold, pred1, pred2):

    test_1_pos = 0
    test_2_pos = 0

    for gold_tag, pred1_tag, pred2_tag in zip(gold, pred1, pred2):

        if pred1_tag != pred2_tag:
            if pred1_tag == gold_tag:
                test_1_pos += 1
            elif pred2_tag == gold_tag:
                test_2_pos += 1

    print(test_1_pos, test_2_pos)
    assert test_1_pos+test_2_pos >= 25

    mc_nemar_stat = (abs(test_1_pos-test_2_pos)-1)**2/(test_1_pos+test_2_pos)
    # ## without continuity correction:
    # mc_nemar_stat = (test_1_pos-test_2_pos)**2/(test_1_pos+test_2_pos)
    print(mc_nemar_stat)
    print(1 - stats.chi2.cdf(mc_nemar_stat, 1))
    print(1 - stats.chi2.cdf(mc_nemar_stat, 1) < 0.05)

if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument('dataset')
    parser.add_argument('testset')
    parser.add_argument('experiment_one')
    parser.add_argument('experiment_two')
    args, _ = parser.parse_known_args()

    ### get gold data
    gold_data = []
    with open(experiment_settings.filenames['goldfile'].format(textname=args.dataset, testset=args.testset), 'r', newline='') as goldfilehandle:

        reader = csv.reader(goldfilehandle, delimiter='\t')

        curr_sent = []
        for line in reader:
            # if line: ## when pasting norm results, empty line contain tab
            if any(line):
                curr_sent.append([line[0], line[3]])
            else:
                gold_data.append(curr_sent)
                curr_sent = []
    gold_data = [word[1] for sent in gold_data for word in sent]

    experiment_one_pred = [word[1] for sent in eval.get_tagging_predictions(args.experiment_one, args.dataset, args.dataset, args.testset) for word in sent]
    experiment_two_pred = [word[1] for sent in eval.get_tagging_predictions(args.experiment_two, args.dataset, args.dataset, args.testset) for word in sent]

    get_mc_nemar_stats(gold_data, experiment_one_pred, experiment_two_pred)
