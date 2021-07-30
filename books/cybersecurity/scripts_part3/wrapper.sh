#!/bin/bash -
#
# Description:
# Example of executing an encrypted "wrapped" script
#
# Usage:
#   wrapper.sh
#       Enter the password when prompted
#

encrypted='U2FsdGVkX1924mPW0reox80nTE8S+QyPt4aDF3Df3MEdwYOz+2zeqEiCFG6yRISh
nAvFG20uFcmWXv6CTzabaEuCbR0B+kDdOsrOum/o9NvWTF6ligFcN4eQZnAh087K'

read -s word

innerScript=$(echo "$encrypted" | openssl aes-256-cbc -base64 -d -pass pass:"$word")

eval "$innerScript"
