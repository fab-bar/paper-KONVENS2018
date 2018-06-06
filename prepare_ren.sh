# Download ReN 0.6
wget http://hdl.handle.net/11022/0000-0007-C64E-3@ZIP -O CorAXML-0.6.zip

unzip CorAXML-0.6.zip
mv CoraXML/ReN_2018-03-07 .
rm -r CoraXML
mkdir ReN_2018-03-07_rest
grep -L -Z -r 'time:14/[12]' ./ReN_2018-03-07 | xargs -0 -I{} mv {} ReN_2018-03-07_rest
grep -L -Z -r 'genre:P' ./ReN_2018-03-07 | xargs -0 -I{} mv {} ReN_2018-03-07_rest

python3 extract_tokens_from_coraxml.py ReN_2018-03-07/ ren ren --outfolder data
python3 extract_tokens_from_coraxml.py ReN_2018-03-07_rest/ ren ren_background --nosplit --outfolder data

### remove archive and folders
rm -r CorAXML-0.6.zip ReN_2018-03-07 ReN_2018-03-07_rest
