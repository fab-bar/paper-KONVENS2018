# Downlad ReM 1.0
wget https://zenodo.org/record/3624693/files/rem-corralled-20161222.tar.xz

tar xf rem-corralled-20161222.tar.xz
rm rem-corralled-20161222/README.md
mkdir rem-corralled-20161222_rest
grep -L -Z -r '<corpus>MiGraKo' ./rem-corralled-20161222 | xargs -0 -I{} mv {} rem-corralled-20161222_rest
grep -L -Z -r '<genre>P</genre>' ./rem-corralled-20161222 | xargs -0 -I{} mv {} rem-corralled-20161222_rest
grep -L -Z -r '<language-type>oberdeutsch' ./rem-corralled-20161222 | xargs -0 -I{} mv {} rem-corralled-20161222_rest
grep -L -Z -r '<time>13,1' ./rem-corralled-20161222 | xargs -0 -I{} mv {} rem-corralled-20161222_rest

python3 extract_tokens_from_coraxml.py rem-corralled-20161222/ rem rem --outfolder data
python3 extract_tokens_from_coraxml.py rem-corralled-20161222_rest/ rem rem_background --nosplit --outfolder data

### remove archive and folders
rm -r rem-corralled-20161222.tar.xz rem-corralled-20161222 rem-corralled-20161222_rest
