
set terminal svg 
set grid ytics
set key below 
set ylabel 'Cell Voltage [V]' 
set out 'path/plot.svg' 
set multiplot layout 3,1   
set lmargin 10.84
set bmargin 0
set format y "%4.3f"
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x ""
set nokey  

plot "path/plot.txt" using 1:3  with lines title "cell 1", \
     "path/plot.txt" using 1:4  with lines title "cell 2", \
     "path/plot.txt" using 1:5  with lines title "cell 3", \
     "path/plot.txt" using 1:6  with lines title "cell 4", \
     "path/plot.txt" using 1:7  with lines title "cell 5", \
     "path/plot.txt" using 1:8  with lines title "cell 6", \
     "path/plot.txt" using 1:9  with lines title "cell 7", \
     "path/plot.txt" using 1:10 with lines title "cell 8"
unset ylabel
set ylabel 'Current [A]'
 
unset key

set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%m/%d\n%H:%M"

plot "path/plot.txt" using 1:12  with lines title "Current"

unset multiplot
set out

