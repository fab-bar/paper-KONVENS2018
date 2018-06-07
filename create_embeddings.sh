cut -f1 data/rem_background | tr '\n' ' ' | sed 's/  /\n/g' > data/rem_background_text
mkdir -p data/embeddings/rem_background/
cd lib/hyperwords
source .venv/bin/activate
bash corpus2svd.sh ../../data/rem_background_text ../../data/embeddings/rem_background/svd
bash corpus2sgns.sh ../../data/rem_background_text ../../data/embeddings/rem_background/sgns
deactivate
cd ../..
mkdir -p data/embeddings/rem_background/fasttext
cd lib/fastText
./fasttext skipgram -input ../../data/rem_background_text -output ../../data/embeddings/rem_background/fasttext/rem
cd ../..

cut -f1 data/ren_background | tr '\n' ' ' | sed 's/  /\n/g' > data/ren_background_text
mkdir -p data/embeddings/ren_background/
cd lib/hyperwords
source .venv/bin/activate
bash corpus2svd.sh ../../data/ren_background_text ../../data/embeddings/ren_background/svd
bash corpus2sgns.sh ../../data/ren_background_text ../../data/embeddings/ren_background/sgns
deactivate
cd ../..
mkdir -p data/embeddings/ren_background/fasttext
cd lib/fastText
./fasttext skipgram -input ../../data/ren_background_text -output ../../data/embeddings/ren_background/fasttext/ren
cd ../..

cd data
rm rem_background_text rem_background_text.clean \
   ren_background_text ren_background_text.clean
cd ..
