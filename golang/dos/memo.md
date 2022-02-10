gnuplot -e 'set terminal png; set logscale xy; set output "./temperature_log.png"; set xlabel "time [s]"; set ylabel "temperature [°C]"; set yrange [40:70]; plot "temperature" using 0:($2/1000) title "temperature"'

gnuplot -e 'set terminal png; set logscale xy; set output "./temperature_detail_log.png"; set xlabel "time [s]"; set ylabel "temperature [°C]"; set xrange [0.3:82]; set yrange [48:62]; plot "temperature_detail" using ($0/10):($2/1000) title "temperature"'


gnuplot -e 'set terminal png; set logscale xy; set output "./temperature_detail_log.png"; set xlabel "time [s]"; set ylabel "temperature [°C]"; set ytics (48,50,52,54,56,58,60,62); set xrange [0.3:82]; set yrange [48:62]; plot "temperature_detail" using ($0/10):($2/1000) title "temperature"'


gnuplot -e 'set terminal png; set output "./temperature_detail.png"; set xlabel "time [s]"; set ylabel "temperature [°C]"; set yrange [48:62]; plot "temperature_detail" using ($0/10):($2/1000) title "temperature"'

$$
\log(y) = a*\log(x) \\
y = x^a
$$

gnuplot -e 'f(x)=a*x**b; fit[2:1500] f(x) "temperature" using ($0/10):($2/1000) via a,b; set terminal png; set output "./temperature_fit.png"; set xlabel "time [s]"; set ylabel "temperature [°C]"; set yrange [48:62]; plot "temperature" using ($0/10):($2/1000) title "temperature", f(x)'

gnuplot -e 'f(x)=a*x**b+c; fit[20:1500] f(x) "temperature" using 0:($2/1000) via a,b,c; set terminal png; set output "./temperature_fit.png"; set yrange [45:70]; set xlabel "time [s]"; set ylabel "temperature [°C]"; set key right bottom; plot "temperature" using 0:($2/1000) title "temperature", f(x) lw 5'


f(x)=a*x**b; fit[1:1500] f(x) "temperature_detail" using ($0/10):($2/1000) via a,b

