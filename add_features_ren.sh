cp data/ren_train data/ren_train_without_additional_features
cp data/ren_devel data/ren_devel_without_additional_features
cp data/ren_test data/ren_test_without_additional_features

function add_empty_column() {
    python3 add_empty_column.py data/ren_$1 > data/ren_${1}_tmp
    mv data/ren_${1}_tmp data/ren_$1
}

## 1. automatic normalization -- NA

add_empty_column train
add_empty_column devel
add_empty_column test

add_empty_column train
add_empty_column devel
add_empty_column test

## 2. tags given by other tagger (for orig, simpl and norm) -- NA

add_empty_column train
add_empty_column devel
add_empty_column test

add_empty_column train
add_empty_column devel
add_empty_column test

add_empty_column train
add_empty_column devel
add_empty_column test

add_empty_column train
add_empty_column devel
add_empty_column test

add_empty_column train
add_empty_column devel
add_empty_column test

## 3. gold spellvarsubstitution

python3 add_gold_spellvar.py data/ren_train data/ren_devel 1 4 6 > data/ren_devel_tmp
mv data/ren_devel_tmp data/ren_devel

python3 add_gold_spellvar.py data/ren_train data/ren_test 1 4 6 > data/ren_test_tmp
mv data/ren_test_tmp data/ren_test

## 4. gold posmorph substitution

python3 add_gold_spellvar.py data/ren_train data/ren_devel 1 4 5 > data/ren_devel_tmp
mv data/ren_devel_tmp data/ren_devel

python3 add_gold_spellvar.py data/ren_train data/ren_test 1 4 5 > data/ren_test_tmp
mv data/ren_test_tmp data/ren_test

## 5. gold pos substitution

python3 add_gold_spellvar.py data/ren_train data/ren_devel 1 4 4 > data/ren_devel_tmp
mv data/ren_devel_tmp data/ren_devel

python3 add_gold_spellvar.py data/ren_train data/ren_test 1 4 4 > data/ren_test_tmp
mv data/ren_test_tmp data/ren_test

## 6. Spellvardetection - exact (POS + morph + lemma)

python3 add_detected_spellvar.py data/ren_train data/ren_devel data/ren_devel_spellvars_exact 1 > data/ren_devel_tmp
python3 add_detected_spellvar.py data/ren_train data/ren_test data/ren_test_spellvars_exact 1 > data/ren_test_tmp
mv data/ren_devel_tmp data/ren_devel
mv data/ren_test_tmp data/ren_test

## 7. Spellvardetection - exact (norm)

add_empty_column devel
add_empty_column test

## 8. Spellvardetection - approx (POS)

python3 add_detected_spellvar.py data/ren_train data/ren_devel data/ren_devel_spellvars_pos 1 > data/ren_devel_tmp
python3 add_detected_spellvar.py data/ren_train data/ren_test data/ren_test_spellvars_pos 1 > data/ren_test_tmp
mv data/ren_devel_tmp data/ren_devel
mv data/ren_test_tmp data/ren_test
