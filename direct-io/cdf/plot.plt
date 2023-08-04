set term postscript eps color 25 font ",32"
set title "CDF of IO latency"
set ylabel 'cumulative distribution'
set xlabel 'IO latency (ms)'
set yrange [0:1]
set xrange [0:20]

set size 1.2, 1.3
set ytic 0,0.2,1
set xtic (0,5,10,15,20)
set key bottom right
set grid

set output 'cdf.eps'

plot \
'./sorted.cdf'  u (($2)/1000):($1) title "sorted" w l lw 6 lc rgb 'blue', \
'./random.cdf'  u (($2)/1000):($1) title "unsorted" w l lw 6 lc rgb 'red', \