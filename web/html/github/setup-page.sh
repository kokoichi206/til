#!/bin/bash

names=("YuichirouSeitoku" "Shimpei-GANGAN" "kokoichi206" "kqns91" "husita-h" "p238049y")

target_html="gh_index_base.html"

for name in "${names[@]}"
do
    tmp="${target_html}_${name}"
    cp "${target_html}" "${tmp}"
    sed -i "s@:user-name:@${name}@g" "${tmp}"

    sudo mv "${tmp}" /var/www/html/github/${name}/index.html
done
