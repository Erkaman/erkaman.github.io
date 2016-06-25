#!/usr/local/bin/gnuplot
reset

set terminal svg size 410,250 fname 'Verdana, Helvetica, Arial, sans-serif' \
fsize '10' rounded dashed
set output 'out.svg'

#grid
set style line 12 lc rgb '#808080' lt 0 lw 1
set grid ytics back ls 12

# line styles:
# ps = point-size
# pt = point-type
# lw = line-width
# lt = line-type
# ps = point-size
set style line 1 lc rgb '#7b1a0e' pt 1 ps 1 lt 1 lw 2
set style line 2 lc rgb '#5e8c36' pt 6 ps 1 lt 1 lw 2
set style line 3 lc rgb '#2e269c' pt 4 ps 1 lt 1 lw 2

set key at 7.5,75000 box opaque
set border back

set xlabel 'Data size'
set ylabel 'Compression time(microseconds)'
set xrange [4:10]
set yrange [0:80000]

set xtics (\
'10K' 0 ,'50K' 1, '100K' 2, '200K' 3, '500K' 4,\
'1M' 5, '2M' 6, '5M' 7, '10M' 8, '20M' 9, '40M' 10)
set ytics 10000

plot 'data.dat'  using 1:2 t 'Random CPU' w lp ls 1, \
     ''          using 1:4 t 'Random GPU' w lp ls 2,\
     ''          using 1:5 t 'Compressible GPU' w lp ls 3
