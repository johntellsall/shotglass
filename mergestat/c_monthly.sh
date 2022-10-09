# using gnuplot, plot csv file "x.csv"
# columns seperated by comma
# output png
# field 1 is date formatted 'YYYY-MM'
# field 2 is number of commits
# output format "YYYY-MM"
# title beer

gnuplot <<EOF
set title "Flask Monthly Commits"
set ylabel "Commits per Month"
set xlabel "Month"
set output "c_monthly.png"

set key off
set terminal png size 800,600
set datafile separator ","
set xdata time
set timefmt "%Y-%m"
plot 'c_monthly.csv' using 1:2 with lines
EOF

echo DONE
