# using gnuplot, plot csv file "x.csv"
# columns seperated by comma
# output png

gnuplot <<EOF
set terminal png
set output "c_monthly.png"
set datafile separator ","
plot 'c_monthly.csv' using 1:2 with lines
EOF
