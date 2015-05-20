#!/usr/bin/env bash

# ADD DETOKENIZING

./sample.py --source=newstest/ntst14.en --beam-search --beam-size 10 --trans newstest/result.fr --state search_state.pkl search_model.npz
cd newstest
./wrap-xml.perl fr newstest2014-fren-src.en.sgm ref < ntst14.fr > newstest2014-fren-ref.fr.sgm
sed -i 's/tstset/refset/g' newstest2014-fren-ref.fr.sgm
./wrap-xml.perl fr newstest2014-fren-src.en.sgm ref < result.fr > newstest2014-fren-tst.fr.sgm
cd ../mteval-v13a-20091001
./mteval-v13a.pl -r ../newstest/newstest2014-fren-ref.fr.sgm -s ../newstest/newstest2014-fren-src.en.sgm -t ../newstest/newstest2014-fren-tst.fr.sgm -b