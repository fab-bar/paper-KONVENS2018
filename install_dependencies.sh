mkdir lib
cd lib

## spellvardetection
git clone https://github.com/fab-bar/SpellvarDetection.git
cd SpellvarDetection
git checkout fe5dea89977bb45b2c88cbdc520653a2c472357b
python3 -m venv .venv
source .venv/bin/activate
pip install pipenv
pipenv install
deactivate
cd ..

## normalization
git clone https://github.com/moses-smt/mgiza.git
cd mgiza/mgizapp
git checkout d643960de98565d208114780ba8025799208afa7
cmake .
make
make install
cd inst
mv scripts/* .
mv bin/* .
rm -r scripts
rm -r bin
cd ../../..

git clone https://github.com/moses-smt/mosesdecoder.git
cd mosesdecoder
git checkout ae7aa6a9d25be49ab4c15ec68515e74490af399b
./bjam --max-kenlm-order=10
cd ..

git clone https://github.com/clarinsi/csmtiser.git
cd csmtiser
git checkout 16c0cd3471baa82eb5f63e29a0c579801d2df2b5
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

## embedding experiments
git clone https://github.com/lukaselmer/hyperwords
cd hyperwords
git checkout bc7a84beccede98fecfe1ff3a60ada46650df6da
chmod +x scripts/*
virtualenv .venv
source .venv/bin/activate
pip install numpy scipy sparsesvd docopt
deactivate

git clone https://github.com/BIU-NLP/word2vecf.git
git checkout e075b2cc96c6b5aede4dfe83585aceadf14ce570
make -C word2vecf
cd ..

git clone https://github.com/facebookresearch/fastText.git
cd fastText
git checkout v0.1.0
make
cd ..

# Tagger

## TreeTagger
mkdir TreeTagger
cd TreeTagger
wget https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.3.tar.gz
wget https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz
wget https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh
wget https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/middle-high-german.par.gz
sh install-tagger.sh
cd ..

## RFTagger
wget https://www.cis.uni-muenchen.de/~schmid/tools/RFTagger/data/RFTagger.zip
unzip RFTagger.zip
rm RFTagger.zip

## HunPos
git clone https://github.com/mivoq/hunpos.git
cd hunpos
git checkout 0f0f775039fa749e67711c07ac681a16c0979349
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=install
make
make install
cd ../..

## Marmot
git clone https://github.com/muelletm/cistern.git
cd cistern
git checkout a9f745631570cabb0afb88292ea2dc8abeafb4a9
cd marmot
ant
mv marmot-`date +"%Y-%m-%d"`.jar marmot.jar
cd ../..

cd ..
