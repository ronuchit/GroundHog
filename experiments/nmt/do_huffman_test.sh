#!/usr/bin/env bash

cd newstest
python ../bitexts/huffman/huffman.py ntst14.en en ../bitexts/huffman/en_huff_enc.pkl -e
cd ..

./sample.py --source=newstest/en_encoded.txt --beam-search --beam-size 10 --trans newstest/fr_encoded.txt --state huffsearch_state.pkl huffsearch_model.npz

cd newstest
python ../bitexts/huffman/huffman.py fr_encoded.txt fr ../bitexts/huffman/fr_huff_dec.pkl -d
mv fr_decoded.txt result.fr
rm en_encoded.txt fr_encoded.txt
cd ..

printf "Tokenized\n"
cd newstest
./wrap-xml.perl fr newstest2014-fren-src.en.sgm ref < ntst14.fr > newstest2014-fren-ref.fr.sgm
sed -i 's/tstset/refset/g' newstest2014-fren-ref.fr.sgm
./wrap-xml.perl fr newstest2014-fren-src.en.sgm ref < result.fr > newstest2014-fren-tst.fr.sgm
cd ../mteval-v13a-20091001
./mteval-v13a.pl -r ../newstest/newstest2014-fren-ref.fr.sgm -s ../newstest/newstest2014-fren-src.en.sgm -t ../newstest/newstest2014-fren-tst.fr.sgm -b

printf "\n\n\nDetokenized\n"
cd ../newstest
../web-demo/detokenizer.perl -l fr < ntst14.fr > ntst14_detok.fr
./wrap-xml.perl fr newstest2014-fren-src.en.sgm ref < ntst14_detok.fr > newstest2014-fren-ref.fr.sgm
sed -i 's/tstset/refset/g' newstest2014-fren-ref.fr.sgm
../web-demo/detokenizer.perl -l fr < result.fr > result_detok.fr
./wrap-xml.perl fr newstest2014-fren-src.en.sgm ref < result_detok.fr > newstest2014-fren-tst.fr.sgm
rm ntst14_detok.fr result_detok.fr
cd ../mteval-v13a-20091001
./mteval-v13a.pl -r ../newstest/newstest2014-fren-ref.fr.sgm -s ../newstest/newstest2014-fren-src.en.sgm -t ../newstest/newstest2014-fren-tst.fr.sgm -b