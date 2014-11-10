#
# Score vs. Date Introduced
#

set title "Score vs. Date Introduced"
set key bottom right
set mxtics 10
set mytics 10
set grid
set xlabel "Degree"
set ylabel "Count"
set tics scale 2
set terminal png size 1500,800
set output 'billscores.png'
plot  "billscores.tab" using 1:2 title "" with points pt 6
