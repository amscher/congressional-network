#
# Score vs. Date Introduced
#

set title "Fraction of Bills vs. Date Introduced"
set xdata time
set timefmt "%Y-%m-%d"
set format x "%Y-%m-%d"
set key top right
set mxtics 10
set mytics 10
set grid
set xlabel "Date Introduced"
set ylabel "Fraction of Bills"
set tics scale 1
set terminal png size 1500,1000
set output '113/enacted.png'
plot "billcount5.tab" using 1:2 title "enacted" with points pt 6