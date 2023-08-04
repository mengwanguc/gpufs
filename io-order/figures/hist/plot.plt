set title "Time to read 10000 random files from Imagenet from disk\n{/*0.8 we use the same 10000 files for all measurements}" font ",18"
set terminal postscript eps enhanced color 22 font ",15"
set output "eps/plot.eps"

set boxwidth 1
set style fill pattern border
set key top right horizontal outside

set ylabel "Time cost (sec)"

set yrange [0 : 100]
#set xtics 3
set xrange [9 : 16]
set xtics format ""
#set logscale y 10
#set format y "10^{%L}"
set bmargin 3

set xtics ('8+2'  11, \
           "16+2"  14)

set ytic 0,20,100
           
set size 0.6,0.50
set origin 0.1,0.1


set arrow 1 from 11.25,44 to 11.25,41 lc rgb 'red' size screen 0.03,10
set label '8%' at 11.4,44 tc rgb 'red' font ",12"

set arrow 2 from 14.25,85 to 14.25,72 lc rgb 'red' size screen 0.03,10
set label '16%' at 14.4,75 tc rgb 'red' font ",12"

plot \
'dat/unsorted.txt' u 1:2 with boxes title "To degraded" fc rgb "blue" fs solid , \
'dat/to-healthy.dat' u 1:2 with boxes title "To healthy" fc rgb "green" fs solid , \