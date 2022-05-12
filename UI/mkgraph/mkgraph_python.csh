#!/bin/csh -f 

set j = $1 
@ i = $j / 24 + 1 
@ k = $j * 59 
rm path/*.csv
rm path/plot*

while($i >= 0)

cp path/`date +\%Y\%m\%d -d "$i"' days ago'`.csv path/
sed -e 's/,//g' path/`date +\%Y\%m\%d -d "$i"' days ago'`.csv >> path/plot~.txt
@ i --
end

tail -n $k path/plot~.txt > path/plot.txt

gnuplot path/mkgraph.gp 

tail -n 1 path/plot.txt | awk ' { print $15 }' >  path/FLAG


