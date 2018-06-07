function create_config() {
    cat > lib/csmtiser/config.yml <<- EOF
# -*- coding: utf-8 -*-

# Configuration file of the normaliser. The paths to Moses components and various parameters are set here.

# Absolute path to the directory in which the models should be created
working_dir: ${PWD}/data/norm_model/rem_${1}

# Encoding of all the datasets
encoding: utf8

# the character to be used internally for marking word boundaries
# this must be a single character that is different from the space character and does not appear anywhere in the corpus
# usually, the underscore (_) is a good choice, but as it occurs in the example Slovene twitter file we use the pound sign here
tokenseparator: £

# Whether the data has to be tokenised, ie. spaces put before punctuation etc.
tokenise: False

# Whether the data should be truecased.
truecase: False
# Location of the dataset on which truecasing should be learnt, if no dataset (or model) is given, truecasing is learnt on both sides of the training data
truecase_dataset: ${PWD}/data/rem_train_${1} ## does not work if no dataset is given (despite truecase=false)
# If you already have a truecasing model available, just give its path and that model will be used
truecase_model: null

# Whether the data should be lowercased, if the data is written in non-standard orthography (like Twitter data), this is probably a good idea, however, all normalisation will therefore be lowercased as well
lowercase: True

# Whether the output should be verticalised and token-aligned
align: False

# Training datasets
train_orig: ${PWD}/data/rem_train_${1}
train_norm: ${PWD}/data/rem_train_norm

# Percentage of training data to be used for development set (for tuning the system)
# If you have a dev set aside of the training data, define the path in the dev variable
dev_perc: 0.1
dev_orig: null
dev_norm: null

# Location of the datasets for language modeling, the target-side training data is always used (does not have to be defined)
# Experiments show that using multiple relevant target-language datasets as language models is the easiest way to improve your results
lms: []

# Order of the language model, if you have compiled KenLM allowing orders higher than 6, order 10 has shown to yield best results
lm_order: 10

# Location of the Moses scripts
moses_scripts: ${PWD}/lib/mosesdecoder/scripts/

# Location of the KenLM tool for language modeling (by default installed with Moses)
kenlm: ${PWD}/lib/mosesdecoder/bin/

# Location of the Moses decoder, mostly same as location of KenLM
moses: ${PWD}/lib/mosesdecoder/bin/

# Location of mgiza
mgiza: ${PWD}/lib/mgiza/mgizapp/inst/

# Number of CPU cores to use during training and tuning
num_cores: 3
EOF
}

cut -f1 data/rem_train > data/rem_train_orig
cut -f2 data/rem_train > data/rem_train_simple
cut -f3 data/rem_train > data/rem_train_norm

cut -f1 data/rem_devel > data/rem_devel_orig
cut -f2 data/rem_devel > data/rem_devel_simple
cut -f1 data/rem_test > data/rem_test_orig
cut -f2 data/rem_test > data/rem_test_simple

for type in orig simple; do

    mkdir -p data/norm_model/rem_${type}

    create_config ${type}

    cd lib/csmtiser
    source .venv/bin/activate
    python preprocess.py
    python train.py
    python normalise.py ../../data/rem_devel_${type}
    python normalise.py ../../data/rem_test_${type}
    deactivate
    cd ../..
done

cd data
rm rem_train_orig rem_train_simple rem_train_norm \
   rem_devel_orig rem_devel_simple rem_test_orig rem_test_simple \
   rem_train_orig.lower rem_train_simple.lower rem_train_norm.lower \
   rem_train_orig.lower.train rem_train_orig.lower.dev \
   rem_train_simple.lower.train rem_train_simple.lower.dev \
   rem_train_norm.lower.train rem_train_norm.lower.dev \
   rem_devel_orig.lower rem_devel_orig.lower.proc rem_devel_orig.lower.proc.norm \
   rem_devel_simple.lower rem_devel_simple.lower.proc rem_devel_simple.lower.proc.norm \
   rem_test_orig.lower rem_test_orig.lower.proc rem_test_orig.lower.proc.norm \
   rem_test_simple.lower rem_test_simple.lower.proc rem_test_simple.lower.proc.norm
cd ..
