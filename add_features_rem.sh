cp data/rem_train data/rem_train_without_additional_features
cp data/rem_devel data/rem_devel_without_additional_features
cp data/rem_test data/rem_test_without_additional_features

function add_empty_column() {
    python3 add_empty_column.py data/rem_$1 > data/rem_${1}_tmp
    mv data/rem_${1}_tmp data/rem_$1
}

## 1. automatic normalization
function add_norm() {
    paste data/rem_${1} data/rem_${1}_${2}.norm > data/rem_${1}_norm
    mv data/rem_${1}_norm data/rem_${1}
}

add_empty_column train
add_norm devel orig
add_norm test orig

add_empty_column train
add_norm devel simple
add_norm test simple

## 2. tags given by tree tagger for (automatic) normalization
function add_tags() {
    python3 add_treetagger_tags.py data/rem_train $1 lib/TreeTagger lib/TreeTagger/lib/middle-high-german-utf8.par > data/rem_train_tmp
    python3 add_treetagger_tags.py data/rem_devel $1 lib/TreeTagger lib/TreeTagger/lib/middle-high-german-utf8.par > data/rem_devel_tmp
    python3 add_treetagger_tags.py data/rem_test $1 lib/TreeTagger lib/TreeTagger/lib/middle-high-german-utf8.par > data/rem_test_tmp

    mv data/rem_train_tmp data/rem_train
    mv data/rem_devel_tmp data/rem_devel
    mv data/rem_test_tmp data/rem_test
}

add_tags 3 # norm
add_tags 1 # orig
add_tags 2 # simpl
add_tags 7 # autonorm
add_tags 8 # autonorm_simpl

## 3. gold spellvarsubstitution

python3 add_gold_spellvar.py data/rem_train data/rem_devel 1 4 6 > data/rem_devel_tmp
mv data/rem_devel_tmp data/rem_devel

python3 add_gold_spellvar.py data/rem_train data/rem_test 1 4 6 > data/rem_test_tmp
mv data/rem_test_tmp data/rem_test

## 4. gold posmorph substitution

python3 add_gold_spellvar.py data/rem_train data/rem_devel 1 4 5 > data/rem_devel_tmp
mv data/rem_devel_tmp data/rem_devel

python3 add_gold_spellvar.py data/rem_train data/rem_test 1 4 5 > data/rem_test_tmp
mv data/rem_test_tmp data/rem_test

## 5. gold pos substitution

python3 add_gold_spellvar.py data/rem_train data/rem_devel 1 4 4 > data/rem_devel_tmp
mv data/rem_devel_tmp data/rem_devel

python3 add_gold_spellvar.py data/rem_train data/rem_test 1 4 4 > data/rem_test_tmp
mv data/rem_test_tmp data/rem_test

## 6. Spellvardetection - exact (POS + morph + lemma)

python3 add_detected_spellvar.py data/rem_train data/rem_devel data/rem_devel_spellvars_exact 1 > data/rem_devel_tmp
python3 add_detected_spellvar.py data/rem_train data/rem_test data/rem_test_spellvars_exact 1 > data/rem_test_tmp
mv data/rem_devel_tmp data/rem_devel
mv data/rem_test_tmp data/rem_test

## 7. Spellvardetection - exact (norm)

python3 add_detected_spellvar.py data/rem_train data/rem_devel data/rem_devel_spellvars_exactnorm 1 > data/rem_devel_tmp
python3 add_detected_spellvar.py data/rem_train data/rem_test data/rem_test_spellvars_exactnorm 1 > data/rem_test_tmp
mv data/rem_devel_tmp data/rem_devel
mv data/rem_test_tmp data/rem_test

## 8. Spellvardetection - approx (POS)

python3 add_detected_spellvar.py data/rem_train data/rem_devel data/rem_devel_spellvars_pos 1 > data/rem_devel_tmp
python3 add_detected_spellvar.py data/rem_train data/rem_test data/rem_test_spellvars_pos 1 > data/rem_test_tmp
mv data/rem_devel_tmp data/rem_devel
mv data/rem_test_tmp data/rem_test
