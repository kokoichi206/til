dir=$1
cd $dir
pdftoppm -png ./daily.pdf image
cd -
rm $dir/daily.pdf
