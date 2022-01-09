
とりあえず、www-dataで動くかみたほうがいいのと、上位ディレクトリでotherはじいてる可能性

APACHE_RUN_USER と GROUP は www-data でした


まー今の手持ちの情報からするに、純粋にパーミッションを整理していって動くように調整するのが良さそうな気がする

20:13 たけまるサブ sudo -u www-data update_blog.sh
20:13 たけまるサブ してって動くまで調整したらいいんじゃないかな

exec sudo -u root update_blog.sh &

sudousers いじる方針？

