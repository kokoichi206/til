#!/bin/bash

touch count
TMP="$(cat count)"
echo $((TMP + 1)) > count
