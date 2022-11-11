#!/bin/bash

gcc crypto100.c -o decrypt
encrypted="ruoYced_ehpigniriks_i_llrg_stae"
for i in {1..20}; do
    ./decrypt "$encrypted" "$i"
    echo ""
done
