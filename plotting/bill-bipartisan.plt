#
#

set title "% Enacted vs. Partisan Score"
set key top right
set mxtics 10
set mytics 10
set grid
set xlabel "Partisan Score"
set ylabel "% Enacted"
set tics scale 1
set terminal png size 1500,1000
set output 'bill-bipartisan-count.png'
plot "bill-bipartisan-count.tab" using 1:2 title "" pt 7 ps 4