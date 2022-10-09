
set terminal pngcairo size 1500,1000 enhanced font 'Verdana,20'

# set timefmt "%Y-%m-%d %H:%M:%S"

# x input time format YYYY-MM-DD HH:MM:SS
set xdata time
set timefmt "%Y-%m"

set format x "%Y"

set ylabel "Commits per Month"

set output 'monthly.png'
set datafile separator ","
set key autotitle columnhead

plot 'monthly.csv' using 1:2 with linespoints 


